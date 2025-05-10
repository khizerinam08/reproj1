"""
Command-line interface for the LLM chatbot.
"""
import sys
import os
import time
from typing import Optional, Dict, Any
from colorama import Fore, Style, init as colorama_init

# Add parent directory to path to allow imports from other project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.llm.ollama_client import OllamaClient
from src.memory.conversation import ConversationMemory
from src.utils.helpers import ensure_directory_exists
from src.interface.commands import CommandHandler
from src.retrieval.crime_model_rag import CrimeModelRAG
from src.retrieval.query_processor import CrimeQueryProcessor
from src.retrieval.rag_manager import RAGManager

# Initialize colorama for cross-platform colored terminal text
colorama_init()


class ChatbotCLI:
    """
    Command-line interface for interacting with the LLM chatbot.
    Specialized for crime prediction analysis with conversational capabilities.
    """
    
    def __init__(self, model_name: Optional[str] = None, config_path: str = "config/config.yml", model_path: Optional[str] = None):
        """
        Initialize the chatbot CLI.
        
        Args:
            model_name: Name of the LLM model to use (overrides config)
            config_path: Path to the configuration file
            model_path: Path to the crime prediction model file
        """
        self.ollama_client = OllamaClient(config_path)
        
        # Override model name if provided
        if model_name:
            self.ollama_client.model_name = model_name
            
        self.memory = ConversationMemory()
        
        # Initialize crime model if path is provided
        self.crime_model = None
        if model_path and os.path.exists(model_path):
            self.crime_model = CrimeModelRAG(model_path)
            
        # Initialize query processor and RAG manager
        self.query_processor = CrimeQueryProcessor()
        self.rag_manager = RAGManager(config={})  # Use empty config
            
        self.system_message = """
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

For general queries:
- Provide direct answers without excessive explanation
- Avoid lengthy introductions or conclusions
- Use bullet points for lists rather than paragraphs
"""
        
        # Add system message to memory
        self.memory.add_system_message(self.system_message)
        
        # Define message colors
        self.colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'end': '\033[0m',
            'bold': '\033[1m'
        }
        
        # Set up the command handler
        self.command_handler = CommandHandler(
            llm_client=self.ollama_client,
            crime_model=self.crime_model,
            memory=self.memory,
            query_processor=self.query_processor,
            rag_manager=self.rag_manager,
        )
        
    def process_command(self, command: str) -> bool:
        """
        Process special commands.
        
        Args:
            command: Command string from user
            
        Returns:
            True if a command was processed, False otherwise
        """
        cmd = command.lower().strip()
        
        # Handle built-in commands first
        if cmd in ['exit', 'quit', 'bye']:
            print("Exiting chatbot. Goodbye!")
            return True
            
        if cmd == 'clear':
            self.memory.clear()
            # Re-add the system message
            self.memory.add_system_message(self.system_message)
            # Reset context in the query processor
            self.ollama_client.rag_manager.query_processor.reset_context()
            print("Conversation history cleared.")
            return True
            
        if cmd.startswith('save '):
            filename = cmd[5:].strip()
            if not filename.endswith('.yml'):
                filename += '.yml'
                
            path = os.path.join('data', 'conversations', filename)
            if self.memory.save_conversation(path):
                print(f"Conversation saved to {path}")
            else:
                print("Failed to save conversation.")
            return True
            
        if cmd.startswith('load '):
            filename = cmd[5:].strip()
            if not filename.endswith('.yml'):
                filename += '.yml'
                
            path = os.path.join('data', 'conversations', filename)
            if self.memory.load_conversation(path):
                print(f"Conversation loaded from {path}")
            else:
                print(f"Failed to load conversation from {path}")
            return True
        
        # Check if the command starts with a slash for CommandHandler
        if cmd.startswith('/'):
            response = self.command_handler.process_command(cmd)
            print(f"{self.colors['cyan']}Assistant: {self.colors['end']}{response}")
            return True
            
        return False
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate a response using streaming.
        
        Args:
            user_input: The user's input text
            
        Returns:
            The complete response from the LLM
        """
        # Add user message to conversation memory
        self.memory.add_user_message(user_input)
        
        # Display thinking indicator
        print(f"{self.colors['cyan']}Assistant: {self.colors['end']}", end="", flush=True)
        
        # Get conversation history for context
        conversation_history = [
            {"role": msg.__class__.__name__.replace("Message", "").lower(), 
             "content": msg.content}
            for msg in self.memory.get_messages()
        ]
        
        # Generate streaming response
        start_time = time.time()
        complete_response = ""
        
        try:
            # Get streaming response with RAG integration
            for chunk, full_response in self.ollama_client.generate_streaming_response_with_rag(
                user_input, conversation_history=conversation_history
            ):
                # Print the chunk without a newline
                print(chunk, end="", flush=True)
                complete_response = full_response
                
            # Print newline after response is complete
            print()
            
            # Record timing information
            end_time = time.time()
            print(f"{self.colors['yellow']}[Response time: {end_time - start_time:.2f}s]{self.colors['end']}")
            
            # Add complete response to conversation memory
            self.memory.add_ai_message(complete_response)
            
            return complete_response
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"\n{self.colors['red']}{error_msg}{self.colors['end']}")
            
            # Add error message to conversation memory
            self.memory.add_ai_message(error_msg)
            
            return error_msg
    
    def run(self) -> None:
        """
        Run the interactive chatbot CLI session.
        """
        print(f"{self.colors['bold']}{self.colors['cyan']}Crime Prediction AI Assistant{self.colors['end']}")
        print(f"{self.colors['cyan']}Model: {self.ollama_client.model_name} | Focus: Crime prediction with concise responses{self.colors['end']}")
        print(f"{self.colors['yellow']}Ask about crime risk by location/time or general crime topics.{self.colors['end']}")
        print(f"\n{self.colors['magenta']}Examples:{self.colors['end']}")
        print(f"{self.colors['magenta']}  - Crime risk at 41.8781, -87.6298 tonight 10pm?{self.colors['end']}")
        print(f"{self.colors['magenta']}  - Current global crime trends?{self.colors['end']}")
        print("\nCommands:")
        print(f"{self.colors['green']}  exit, quit, bye{self.colors['end']} - Exit")
        print(f"{self.colors['green']}  clear{self.colors['end']}            - Clear history")
        print(f"{self.colors['green']}  save/load <n>{self.colors['end']} - Save/load conversation")
        print(f"{self.colors['green']}  /help{self.colors['end']}            - Show command help")
        print(f"{self.colors['green']}  /weekly <location>{self.colors['end']} - Weekly crime forecast")
        print("-" * 50)
        
        try:
            while True:
                # Get user input
                user_input = input(f"\n{self.colors['bold']}You: {self.colors['end']}").strip()
                
                # Check for commands
                if self.process_command(user_input):
                    continue
                
                # Process the input and get response
                self.process_user_input(user_input)
                
        except KeyboardInterrupt:
            print("\nExiting chatbot. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


def find_model_path():
    """Find the crime prediction model file."""
    possible_paths = [
        os.path.join(os.getcwd(), "crime_model.pkl"),
        os.path.join(os.getcwd(), "models", "crime_model.pkl"),
        os.path.join(os.getcwd(), "data", "models", "crime_model.pkl")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    print("Warning: Could not find crime_model.pkl. Weekly forecasting will be unavailable.")
    return None


if __name__ == "__main__":
    # Create directory for conversations if it doesn't exist
    ensure_directory_exists(os.path.join('data', 'conversations'))
    
    # Look for the crime model
    model_path = find_model_path()
    
    # Run the CLI
    cli = ChatbotCLI(model_path=model_path)
    cli.run() 