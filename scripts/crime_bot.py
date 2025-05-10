"""
Specialized Crime Detection Chatbot

This script implements a focused crime prediction chatbot that only responds
to crime-related queries and refuses to engage with other topics.
"""
import os
import sys
import time
from typing import List, Dict, Any, Optional

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import the chatbot components
from src.llm.ollama_client import OllamaClient
from src.memory.conversation import ConversationMemory
from src.retrieval.query_processor import CrimeQueryProcessor

class CrimeBot:
    """
    A specialized chatbot focused solely on crime prediction.
    Refuses to engage with off-topic queries to prevent misuse.
    """
    
    def __init__(self, config_path: str = "config/config.yml"):
        """
        Initialize the Crime Detection Bot.
        
        Args:
            config_path: Path to the configuration file
        """
        # Initialize components
        self.ollama_client = OllamaClient(config_path)
        self.memory = ConversationMemory()
        self.query_processor = CrimeQueryProcessor()
        
        # Set specialized system message
        self.system_message = """
        You are a specialized Crime Prediction Assistant with access to a crime prediction model.
        Your sole purpose is to provide crime risk assessments for specific locations and times.
        
        DO NOT engage with any questions that are not related to crime prediction or safety.
        For non-crime related queries, politely explain that you can only discuss crime probability
        and suggest they provide a location and time for a crime risk assessment.
        
        For crime prediction queries, provide detailed assessments based on the data.
        """
        
        # Add system message to memory
        self.memory.add_system_message(self.system_message)
        
    def is_crime_related_query(self, query: str) -> bool:
        """
        Determine if a query is related to crime prediction or safety.
        Uses a stricter criteria than the regular query processor.
        
        Args:
            query: The user's query
            
        Returns:
            True if the query is crime-related, False otherwise
        """
        # First check if it meets the criteria for a crime prediction query
        if self.query_processor.is_crime_prediction_query(query):
            return True
            
        # If not a direct prediction query, check if it's a general
        # crime or safety question that we can still engage with
        query_lower = query.lower()
        
        # Safety keywords that we will still engage with
        safety_keywords = [
            "crime", "safe", "safety", "danger", "dangerous", "risk", 
            "robbery", "theft", "assault", "shooting", "violence", "security"
        ]
        
        # Check if any safety keywords are present
        if any(keyword in query_lower for keyword in safety_keywords):
            # Additional check to avoid non-safety questions that just mention these words
            safety_phrases = [
                "how safe", "is it safe", "safety concerns", "crime rate",
                "risk of crime", "crime statistics", "crime prediction"
            ]
            
            # If it contains a safety phrase, it's likely a valid query
            if any(phrase in query_lower for phrase in safety_phrases):
                return True
        
        # Not a crime-related query
        return False
        
    def get_rejection_response(self, query: str) -> str:
        """
        Generate a polite rejection for non-crime related queries.
        
        Args:
            query: The user's query
            
        Returns:
            A rejection message
        """
        return (
            "I'm specialized in crime prediction only and can't provide information on other topics. "
            "I can help you with questions about crime risk in specific locations and times. "
            "For example, you can ask: 'What's the crime risk at coordinates 41.8781, -87.6298 tonight at 10pm?' "
            "or 'How safe is it to walk in downtown Chicago on Saturday evening?'"
        )
        
    def process_query(self, query: str) -> str:
        """
        Process a user query with specialized filtering and streaming response.
        
        Args:
            query: The user's query
            
        Returns:
            The complete response
        """
        # Add user message to memory
        self.memory.add_user_message(query)
        
        # Get conversation history for context
        conversation_history = [
            {"role": msg.__class__.__name__.replace("Message", "").lower(), 
             "content": msg.content}
            for msg in self.memory.get_messages()
        ]
        
        # Check if the query is crime-related
        is_crime_query = self.is_crime_related_query(query)
        
        if not is_crime_query:
            # For non-crime queries, provide a rejection response
            rejection = self.get_rejection_response(query)
            print(f"Assistant: {rejection}")
            
            # Add rejection to memory
            self.memory.add_ai_message(rejection)
            return rejection
        
        # For crime-related queries, process with RAG and streaming
        print("Assistant: ", end="", flush=True)
        
        # Stream the response
        complete_response = ""
        start_time = time.time()
        
        for chunk, full_response in self.ollama_client.generate_streaming_response_with_rag(
            query, conversation_history=conversation_history
        ):
            print(chunk, end="", flush=True)
            complete_response = full_response
            
        # Add complete response to memory
        end_time = time.time()
        print(f"\n[Response time: {end_time - start_time:.2f}s]")
        
        self.memory.add_ai_message(complete_response)
        return complete_response
        
    def run(self):
        """Run the interactive crime bot session."""
        print("=== Specialized Crime Detection Bot ===")
        print("This bot is focused solely on crime prediction and safety assessments.")
        print("It will only respond to crime-related queries and will politely reject other topics.")
        print("Type 'exit' to quit.")
        print("-" * 50)
        
        try:
            while True:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("Goodbye!")
                    break
                
                # Process the query
                self.process_query(user_input)
                
        except KeyboardInterrupt:
            print("\nExiting. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            
if __name__ == "__main__":
    # Create and run the crime bot
    crime_bot = CrimeBot()
    crime_bot.run() 