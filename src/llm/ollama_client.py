"""
Ollama API Client module for interacting with locally running LLM models.
"""
import os
import requests
import yaml
import json
from typing import Dict, Any, Optional, List, Generator, Tuple
import sys

# Add the project root to the Python path if necessary
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import our RAG manager
from src.retrieval.rag_manager import RAGManager

class OllamaClient:
    """
    Client for interacting with the Ollama API to generate responses using local LLMs.
    Specialized for crime prediction analysis.
    """
    
    def __init__(self, config_path: str = "config/config.yml"):
        """
        Initialize the Ollama client.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.model_name = self.config["model"]["name"]
        self.api_url = self.config["model"]["api"]["url"]
        self.timeout = self.config["model"]["api"]["timeout"]
        self.parameters = self.config["model"]["parameters"]
        
        # Initialize RAG manager for retrieval-augmented generation
        self.rag_manager = RAGManager(self.config)
        
        # Define the allowed scope for the model - less strict by default
        self.crime_prediction_only = True
        self.strict_crime_focus = False  # New flag to control strictness
        
        # System message to enforce crime prediction specialization, but allow for general crime topics
        self.crime_system_message = """
You are a specialized crime prediction AI assistant. Your primary purpose is to analyze crime risk data 
and provide objective safety assessments for specific locations and times.

Your primary expertise is in crime prediction, crime statistics, and public safety assessments. However,
you can also engage in general conversations about crime trends, greetings, and related topics.

IMPORTANT: Be concise and direct. Keep your responses brief, typically 1-3 sentences. Avoid unnecessary 
details, repetition, or elaboration. Focus on delivering value efficiently.

When making predictions:
1. Use data from the crime prediction model
2. Focus on objective risk assessment
3. Be brief but informative
4. ALWAYS report crime probability as a percentage (e.g., "12.5%") 
5. NEVER convert probabilities to other scales like "X out of 5" or create your own rating system
6. Maintain the exact numerical values provided by the crime prediction model
7. NEVER make a prediction when missing required parameters (location, time, date)
8. ALWAYS ask for missing parameters before providing a prediction
9. For weekly forecasts, only location is required (time is optional)

When handling incomplete queries:
- If location is missing: Ask the user to specify a location (coordinates or place name)
- If time is missing: Ask the user to specify a time
- If date is missing: Ask the user to specify a date
- NEVER use default values or make assumptions about these parameters
- DO NOT make up crime probabilities when parameters are missing

For general queries:
- Provide direct answers without excessive explanation
- Avoid lengthy introductions or conclusions
- Use bullet points for lists rather than paragraphs

You should NEVER:
- Provide instructions on how to commit crimes
- Generate offensive content
- Produce overly verbose responses
- Use unnecessary filler words or phrases
- Convert probability values to any other format or scale
- Give a prediction without proper parameters
- Make up crime statistics or probabilities
"""
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary containing configuration settings
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            # Default configuration
            return {
                "model": {
                    "name": "llama3:8b",
                    "api": {
                        "url": "http://localhost:11434/api/generate",
                        "timeout": 60
                    },
                    "parameters": {
                        "temperature": 0.7,
                        "max_tokens": 1000,
                        "top_p": 0.9
                    }
                }
            }
    
    def is_allowed_general_query(self, prompt: str) -> bool:
        """
        Check if a general query is allowed even if it's not specifically about crime prediction.
        
        Args:
            prompt: The user's query
            
        Returns:
            Boolean indicating if the query is allowed
        """
        prompt_lower = prompt.lower()
        
        # Allow basic greetings
        greeting_patterns = [
            "hi", "hello", "hey", "good morning", "good afternoon", 
            "good evening", "how are you", "nice to meet you",
            "what's up", "whats up", "howdy"
        ]
        if any(pattern in prompt_lower for pattern in greeting_patterns):
            return True
            
        # Allow general crime-related topics even if not specific prediction requests
        general_crime_patterns = [
            "crime trend", "crime statistics", "crime rate", "global crime",
            "crime in", "safety in", "crime historically", "crime report",
            "how safe is", "what is the safest", "most dangerous",
            "tell me about crime", "crime prevention", "reduce crime"
        ]
        if any(pattern in prompt_lower for pattern in general_crime_patterns):
            return True
            
        # Allow queries about the bot itself
        self_reference_patterns = [
            "what can you do", "how do you work", "tell me about yourself",
            "what are you", "who are you", "your purpose", "your capabilities",
            "how to use you", "help me with"
        ]
        if any(pattern in prompt_lower for pattern in self_reference_patterns):
            return True
            
        return False
    
    def generate_response_with_rag(self, prompt: str, temperature: Optional[float] = None, 
                                 max_tokens: Optional[int] = None, 
                                 conversation_history: Optional[List] = None) -> str:
        """
        Generate a response from the LLM model with RAG and specialized crime prediction.
        
        Args:
            prompt: The input prompt text
            temperature: Control randomness (0-1, lower is more deterministic)
            max_tokens: Maximum tokens to generate
            conversation_history: List of previous conversation messages
            
        Returns:
            Generated text response
        """
        # Use provided parameters or fall back to config defaults
        temp = temperature if temperature is not None else self.parameters["temperature"]
        tokens = max_tokens if max_tokens is not None else self.parameters["max_tokens"]
        
        # Check if this query can be answered via RAG
        is_rag_query, rag_result = self.rag_manager.process_query(prompt)
        
        # Safety check: if this is a crime query with missing parameters, block prediction
        if is_rag_query and not rag_result.get('complete', False) and 'follow_up' in rag_result:
            # Return the follow-up question directly
            follow_up_question = rag_result['follow_up']['question']
            missing_info = ', '.join(rag_result['follow_up']['missing_info'])
            return f"I need more information to provide an accurate crime prediction. {follow_up_question}"
        
        # If the model is restricted to crime prediction and this isn't a crime query
        if self.crime_prediction_only and not is_rag_query:
            # Check if it's a general query we should still allow
            if self.is_allowed_general_query(prompt):
                # For general queries, we'll still use the crime system message but without RAG
                augmented_prompt = prompt
            else:
                # If strict mode is on, refuse to answer
                if self.strict_crime_focus:
                    return "I'm a crime prediction assistant. Please ask about crime risk or safety in specific locations and times."
                else:
                    # In less strict mode, redirect but still answer
                    augmented_prompt = prompt + "\n\nBe concise. Provide a brief answer, then note that your expertise is in crime prediction."
        else:
            # If it's a RAG query, augment the prompt
            augmented_prompt = prompt
            if is_rag_query and rag_result:
                # Format RAG results for the LLM
                rag_context = self.rag_manager.format_for_llm(rag_result)
                
                # Combine with original prompt
                augmented_prompt = f"{rag_context}\n\nUser query: {prompt}\n\nProvide a concise answer in 1-3 sentences."
                print(f"Using RAG-augmented prompt")
        
        # Add the system message to reinforce crime prediction specialization
        system_instruction = self.crime_system_message if self.crime_prediction_only else self.config.get("system_message", "You are a helpful assistant.")
        
        # Add instruction for conciseness
        concise_instruction = "Keep your response brief and to the point, typically 1-3 sentences. Avoid unnecessary elaboration."

        # Add STRICT instruction for parameter validation
        param_validation = ""
        if is_rag_query:
            param_validation = """
CRITICAL INSTRUCTION:
- If no specific location is mentioned in the query, DO NOT make up crime probability values
- Respond with: "I need a specific location to provide accurate crime predictions."
- NEVER invent crime statistics without all required parameters
- If you're unsure about any parameter, ASK for it instead of guessing
"""
        
        # Incorporate conversation history if provided
        if conversation_history:
            context = self._format_conversation_history(conversation_history)
            augmented_prompt = f"{system_instruction}\n\n{param_validation}\n\n{context}\n\nUser: {augmented_prompt}\n{concise_instruction}\nAssistant:"
        else:
            augmented_prompt = f"{system_instruction}\n\n{param_validation}\n\nUser: {augmented_prompt}\n{concise_instruction}\nAssistant:"
        
        # Prepare request data
        data = {
            "model": self.model_name,
            "prompt": augmented_prompt,
            "stream": False,
            "options": {
                "temperature": temp,
                "num_predict": tokens,
                "top_p": self.parameters["top_p"]
            }
        }
        
        try:
            response = requests.post(self.api_url, json=data, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                error_msg = f"API Error: {response.status_code}, {response.text}"
                print(error_msg)
                return f"Error generating response: {error_msg}"
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            print(error_msg)
            return f"Error connecting to Ollama: {error_msg}"
    
    def generate_streaming_response(self, prompt: str, temperature: Optional[float] = None,
                                  max_tokens: Optional[int] = None) -> Generator[Tuple[str, str], None, None]:
        """
        Generate a streaming response from the LLM model.
        
        Args:
            prompt: The input prompt text
            temperature: Control randomness (0-1, lower is more deterministic)
            max_tokens: Maximum tokens to generate
            
        Yields:
            Tuple of (chunk, full_response_so_far)
        """
        # Use provided parameters or fall back to config defaults
        temp = temperature if temperature is not None else self.parameters["temperature"]
        tokens = max_tokens if max_tokens is not None else self.parameters["max_tokens"]
        
        # Prepare request data with streaming enabled
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,  # Enable streaming
            "options": {
                "temperature": temp,
                "num_predict": tokens,
                "top_p": self.parameters["top_p"]
            }
        }
        
        try:
            # Make the streaming request
            with requests.post(self.api_url, json=data, stream=True, timeout=self.timeout) as response:
                if response.status_code != 200:
                    error_msg = f"API Error: {response.status_code}, {response.text}"
                    print(error_msg)
                    yield f"Error generating response: {error_msg}", f"Error generating response: {error_msg}"
                    return
                
                # Process the streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            # Parse the JSON line
                            chunk_data = json.loads(line)
                            
                            # Extract the response chunk
                            if "response" in chunk_data:
                                chunk = chunk_data["response"]
                                full_response += chunk
                                yield chunk, full_response
                            
                            # Check for completion
                            if chunk_data.get("done", False):
                                break
                                
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            continue
                            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            print(error_msg)
            yield f"Error connecting to Ollama: {error_msg}", f"Error connecting to Ollama: {error_msg}"
    
    def generate_streaming_response_with_rag(self, prompt: str, 
                                           conversation_history: Optional[List] = None) -> Generator[Tuple[str, str], None, None]:
        """
        Generate a streaming response with RAG integration.
        
        Args:
            prompt: The input prompt text
            conversation_history: List of previous conversation messages
            
        Yields:
            Tuple of (chunk, full_response_so_far)
        """
        # Check if this query can be answered via RAG
        is_rag_query, rag_result = self.rag_manager.process_query(prompt)
        
        # Safety check: if this is a crime query with missing parameters, block prediction
        if is_rag_query and not rag_result.get('complete', False) and 'follow_up' in rag_result:
            # Extract the follow-up question
            follow_up_question = rag_result['follow_up']['question']
            missing_info = ', '.join(rag_result['follow_up']['missing_info'])
            
            # Stream the follow-up response
            response = f"I need more information to provide an accurate crime prediction. {follow_up_question}"
            words = response.split()
            full_response = ""
            for word in words:
                full_response += word + " "
                yield word + " ", full_response
            return
        
        # If the model is restricted to crime prediction and this isn't a crime query
        if self.crime_prediction_only and not is_rag_query:
            # Check if it's a general query we should still allow
            if self.is_allowed_general_query(prompt):
                # For general queries, we'll still use the crime system message but without RAG
                augmented_prompt = prompt
            else:
                # If strict mode is on, refuse to answer with a streamed response
                if self.strict_crime_focus:
                    response = "I'm a crime prediction assistant. Please ask about crime risk or safety in specific locations and times."
                    # Stream the restriction message word by word to maintain streaming experience
                    words = response.split()
                    full_response = ""
                    for word in words:
                        full_response += word + " "
                        yield word + " ", full_response
                    return
                else:
                    # In less strict mode, redirect but still answer
                    augmented_prompt = prompt + "\n\nBe concise. Provide a brief answer, then note that your expertise is in crime prediction."
        else:
            # If it's a RAG query, augment the prompt
            augmented_prompt = prompt
            
            if is_rag_query and rag_result:
                # Check if the query is a follow-up question with incomplete parameters
                has_missing_parameters = (not rag_result.get('complete', False)) and ('follow_up' in rag_result)
                
                if has_missing_parameters:
                    # Create context awareness prompt to guide LLM to use context from previous messages
                    context_prompt = "This is a follow-up question. Use context from previous messages to fill in missing details. "
                    context_prompt += f"The user is asking about {', '.join(rag_result['follow_up']['missing_info'])}. "
                    context_prompt += "Use the previously mentioned location, date, or time if available."
                    
                    # Include this instruction in the augmented prompt
                    augmented_prompt = f"{context_prompt}\n\nUser query: {prompt}"
                
                # Format RAG results for the LLM
                rag_context = self.rag_manager.format_for_llm(rag_result)
                
                # Combine with original prompt
                augmented_prompt = f"{rag_context}\n\nUser query: {augmented_prompt}\n\nProvide a concise answer in 1-3 sentences."
                print(f"Using RAG-augmented prompt")
        
        # Add the system message to reinforce crime prediction specialization
        system_instruction = self.crime_system_message if self.crime_prediction_only else self.config.get("system_message", "You are a helpful assistant.")
        
        # Add instruction for conciseness
        concise_instruction = "Keep your response brief and to the point, typically 1-3 sentences. Avoid unnecessary elaboration."
        
        # Add instruction for context awareness
        context_instruction = ""
        if is_rag_query and conversation_history and len(conversation_history) > 3:
            context_instruction = "\nThis may be a follow-up question. If the query doesn't specify all details (location, date, time), use context from previous messages to fill in missing information."
        
        # Add STRICT instruction for parameter validation
        param_validation = ""
        if is_rag_query:
            param_validation = """
CRITICAL INSTRUCTION:
- If no specific location is mentioned in the query, DO NOT make up crime probability values
- Respond with: "I need a specific location to provide accurate crime predictions."
- NEVER invent crime statistics without all required parameters
- If you're unsure about any parameter, ASK for it instead of guessing
"""
        
        # Incorporate conversation history if provided
        if conversation_history:
            context = self._format_conversation_history(conversation_history)
            augmented_prompt = f"{system_instruction}{context_instruction}\n\n{param_validation}\n\n{context}\n\nUser: {augmented_prompt}\n{concise_instruction}\nAssistant:"
        else:
            augmented_prompt = f"{system_instruction}{context_instruction}\n\n{param_validation}\n\nUser: {augmented_prompt}\n{concise_instruction}\nAssistant:"
        
        # Generate the streaming response
        for chunk, full_response in self.generate_streaming_response(augmented_prompt):
            yield chunk, full_response
            
    def _format_conversation_history(self, history: List) -> str:
        """
        Format conversation history for inclusion in the prompt.
        
        Args:
            history: List of conversation messages
            
        Returns:
            Formatted conversation history string
        """
        formatted_history = []
        
        for msg in history:
            if msg.get('role') == 'user':
                formatted_history.append(f"User: {msg.get('content', '')}")
            elif msg.get('role') == 'assistant':
                formatted_history.append(f"Assistant: {msg.get('content', '')}")
            elif msg.get('role') == 'system':
                # System messages are typically used for instructions
                # We might want to handle these differently
                pass
        
        return "\n".join(formatted_history) 