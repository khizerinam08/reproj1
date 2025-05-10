"""
RAG Manager for the chatbot.

This module provides a unified interface for different retrieval mechanisms,
including the crime prediction model.
"""
import os
from typing import Dict, List, Optional, Tuple, Any
import json

from src.retrieval.crime_model_rag import CrimeModelRAG
from src.retrieval.query_processor import CrimeQueryProcessor

class RAGManager:
    """
    Manager for Retrieval-Augmented Generation components.
    Manages different retrieval mechanisms that can feed information to the LLM.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the RAG Manager with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize the RAG components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize the various RAG components."""
        
        # Set up the crime prediction model
        try:
            # Check multiple possible locations for the model
            possible_paths = [
                os.path.join(os.getcwd(), "crime_model.pkl"),
                os.path.join(os.getcwd(), "models", "crime_model.pkl"),
                os.path.join(os.getcwd(), "data", "models", "crime_model.pkl"),
                os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "models", "crime_model.pkl")
            ]
            
            # Get model path from config if available
            if self.config.get("model", {}).get("crime_model_path"):
                model_path = self.config["model"]["crime_model_path"]
                possible_paths.insert(0, model_path)  # Try this path first
            
            # Try each possible path
            model_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if model_path is None:
                print("Crime model not found in any of the expected locations.")
                print("Please place a crime_model.pkl file in one of these locations:")
                for path in possible_paths:
                    print(f"- {path}")
                print("The application will run but crime prediction features will be unavailable.")
                self.crime_model = None
            else:
                self.crime_model = CrimeModelRAG(model_path)
                print(f"Crime prediction model loaded successfully from {model_path}.")
            
            self.query_processor = CrimeQueryProcessor()
            
        except Exception as e:
            print(f"Error loading crime prediction model: {e}")
            print("The application will run but crime prediction features will be unavailable.")
            self.crime_model = None
            self.query_processor = CrimeQueryProcessor()
    
    def process_query(self, query: str) -> Tuple[bool, Optional[Dict]]:
        """
        Process a query and determine if it can be handled by a RAG component.
        
        Args:
            query: The user's query string
            
        Returns:
            Tuple of (is_rag_query, rag_result)
            where rag_result is a dictionary with retrieval information
            or None if not a RAG query
        """
        # First, check if this is a crime prediction query and if we have a model loaded
        if self.crime_model and self.query_processor and self.query_processor.is_crime_prediction_query(query):
            return self._process_crime_query(query)
            
        # Add other RAG methods here in the future
        
        # If no RAG methods match, return false
        return False, None
    
    def _process_crime_query(self, query: str) -> Tuple[bool, Dict]:
        """
        Process a crime-related query.
        
        Args:
            query: The user's query string
            
        Returns:
            Tuple of (True, result_dict) where result_dict contains:
            - complete: Whether all parameters are available
            - params: Extracted parameters
            - explanation: Crime prediction explanation if complete
            - follow_up: Follow-up questions if incomplete
        """
        # Extract parameters from the query
        params = self.query_processor.extract_parameters(query)
        
        # Create the result dictionary
        result = {
            'type': 'crime_prediction',
            'complete': params.get('complete', False),
            'params': params,
        }
        
        # Check if it's a weekly forecast request
        is_weekly_forecast = params.get('is_weekly_forecast', False)
        
        # If parameters are complete, make a prediction
        if result['complete']:
            try:
                # Different handling for weekly forecasts vs. point predictions
                if is_weekly_forecast:
                    # For weekly, we'll handle this in the command handler
                    # Just mark it as a weekly forecast request
                    result['weekly_forecast'] = True
                else:
                    # Regular point prediction
                    probability = self.crime_model.predict_crime_probability(
                        params['date'], params['time'],
                        params['longitude'], params['latitude']
                    )
                    
                    # Generate explanation
                    explanation = self.crime_model.generate_explanation(probability, params)
                    
                    # Add to result
                    result['probability'] = probability
                    result['explanation'] = explanation
            except Exception as e:
                result['error'] = str(e)
                result['complete'] = False
        else:
            # Generate appropriate follow-up questions based on missing information
            missing_info = []
            using_default = params.get('using_default', {})
            
            # Determine what's missing
            if isinstance(using_default, bool):  # For backward compatibility
                if using_default:
                    missing_info.append("location coordinates")
            else:
                if using_default.get('coordinates', False):
                    missing_info.append("location coordinates")
                if using_default.get('time', False) and not is_weekly_forecast:
                    missing_info.append("time")
                if using_default.get('date', False) and not is_weekly_forecast:
                    missing_info.append("date")
            
            # Create a detailed, user-friendly follow-up question
            if is_weekly_forecast and 'location coordinates' in missing_info:
                follow_up_question = (
                    "To generate a weekly crime forecast, I need a specific location. "
                    "Please provide a location by city name or coordinates. "
                    "For example: 'Generate a weekly forecast for downtown Chicago' or "
                    "'Give me a weekly forecast for 41.8781, -87.6298'"
                )
            elif missing_info:
                examples = []
                if 'location coordinates' in missing_info:
                    examples.append("'What's the crime risk at 41.8781, -87.6298?'")
                    examples.append("'Is it safe in downtown Chicago?'")
                if 'time' in missing_info:
                    examples.append("'What's the crime risk at 10pm?'")
                    examples.append("'Is it safe during the morning?'")
                if 'date' in missing_info:
                    examples.append("'What's the crime risk tomorrow?'")
                    examples.append("'Is it safe on Friday?'")
                
                example_text = " or ".join(examples[:2])
                follow_up_question = f"To predict crime risk, I need more information about: {', '.join(missing_info)}. Please provide these details. For example: {example_text}"
            else:
                follow_up_question = "To predict crime risk, I need more specific information. Please provide location, date, and time details."
            
            result['follow_up'] = {
                'missing_info': missing_info,
                'question': follow_up_question
            }
        
        return True, result
    
    def format_for_llm(self, rag_result: Dict) -> str:
        """
        Format the RAG result for use in the LLM prompt.
        
        Args:
            rag_result: The result from the RAG process
            
        Returns:
            Formatted string for the LLM prompt
        """
        # Simple formatting for now
        formatted_text = "### Crime Prediction Context:\n"
        
        # Check if we have incomplete parameters and follow-up suggestions
        if 'follow_up' in rag_result:
            formatted_text += "IMPORTANT: DO NOT MAKE A PREDICTION. Required parameters are missing.\n\n"
            formatted_text += f"Missing information: {', '.join(rag_result['follow_up']['missing_info'])}\n"
            formatted_text += f"Follow-up needed: {rag_result['follow_up']['question']}\n\n"
            formatted_text += "Do not make up any crime probabilities. Ask the user for the missing information.\n"
            return formatted_text
        
        # If probability is available, include it
        if 'probability' in rag_result:
            probability = rag_result['probability']
            probability_percent = probability * 100
            formatted_text += f"Crime probability: {probability_percent:.1f}% (IMPORTANT: always present this exact percentage value in your response)\n\n"
        
        # Include the explanation if available
        if 'explanation' in rag_result:
            formatted_text += f"{rag_result['explanation']}\n\n"
        
        # If it's a weekly forecast request, add special handling instructions
        if rag_result.get('weekly_forecast', False):
            formatted_text += (
                "This is a weekly forecast request. Note that for weekly forecasts, only location is required.\n"
                "Inform the user that the weekly forecast is being processed and will be displayed shortly.\n"
            )
            return formatted_text
            
        # Add specific instruction to preserve probability values and never make up predictions
        formatted_text += (
            "IMPORTANT INSTRUCTIONS:\n"
            "1. When reporting the probability in your response, always use the exact percentage value provided above.\n"
            "2. Never convert to a different scale or format.\n"
            "3. If any parameters are missing, ask for them instead of providing a prediction.\n"
            "4. Never make up crime probabilities - only use the exact values provided.\n"
        )
            
        return formatted_text 