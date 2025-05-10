"""
Test script for the chatbot with RAG integration.

This script demonstrates how the chatbot works with
the crime prediction model integrated via RAG.
"""
import os
import sys
import yaml
from datetime import datetime

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import the chatbot components
from src.llm.ollama_client import OllamaClient
from src.memory.conversation import ConversationMemory
from src.retrieval.rag_manager import RAGManager

def get_user_input(prompt: str = "You: ") -> str:
    """Get input from the user with the given prompt."""
    try:
        return input(prompt).strip()
    except EOFError:
        return "exit"
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

def main():
    """Main function for the chatbot test."""
    print("=== Chatbot with RAG Integration Test ===")
    
    # Load configuration
    config_path = os.path.join(project_dir, "config", "config.yml")
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        print(f"Using model: {config['model']['name']}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Using default configuration")
        config = {}
    
    # Initialize components
    print("Initializing chatbot components...")
    
    # Initialize Ollama client
    ollama_client = OllamaClient(config_path)
    
    # Initialize conversation memory
    memory = ConversationMemory()
    
    # Add system message to set the context
    system_message = (
        "You are a helpful assistant with access to a crime prediction model. "
        "When users ask about crime risk or safety in specific locations and times, "
        "you can provide predictions based on historical data. "
        "For other questions, you'll answer normally."
    )
    memory.add_system_message(system_message)
    
    # Print instructions
    print("\nChatbot ready! Type 'exit' to quit.")
    print("Try asking about crime risk in specific locations and times.")
    print("Example: What's the crime risk at coordinates 41.8781, -87.6298 tomorrow at 8pm?")
    print("Example: How safe is it to walk downtown Chicago at night?")
    print()
    
    # Main chat loop
    while True:
        # Get user input
        user_input = get_user_input("You: ")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # Add user message to memory
        memory.add_user_message(user_input)
        
        # Get conversation history for context
        conversation_history = [
            {"role": msg.__class__.__name__.replace("Message", "").lower(), "content": msg.content}
            for msg in memory.get_messages()
        ]
        
        # Generate response using the LLM with conversation history
        print("Assistant: ", end="", flush=True)
        response = ollama_client.generate_response(
            user_input, 
            conversation_history=conversation_history
        )
        
        # Print the response
        print(response)
        
        # Add assistant response to memory
        memory.add_ai_message(response)
        print()

if __name__ == "__main__":
    main() 