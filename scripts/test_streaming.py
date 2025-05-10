"""
Test script for streaming responses from the LLM chatbot.

This script demonstrates the streaming functionality of the chatbot,
showing how responses are displayed in real-time as they're generated.
"""
import os
import sys
import time

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import the chatbot components
from src.llm.ollama_client import OllamaClient
from src.memory.conversation import ConversationMemory

def get_user_input(prompt: str = "You: ") -> str:
    """Get input from the user with the given prompt."""
    try:
        return input(prompt).strip()
    except EOFError:
        return "exit"
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

def show_streaming_demo():
    """Demonstrate streaming responses from the LLM."""
    print("=== Streaming Response Demo ===")
    
    # Initialize Ollama client
    ollama_client = OllamaClient()
    print(f"Using model: {ollama_client.model_name}")
    
    # Initialize conversation memory
    memory = ConversationMemory()
    
    # Add system message to set the context
    system_message = "You are a helpful assistant. Keep your responses concise and informative."
    memory.add_system_message(system_message)
    
    # Standard (non-streaming) response test
    query = "What is the capital of France?"
    print(f"\nStandard Response Test:")
    print(f"Query: {query}")
    
    print("Response (non-streaming): ", end="", flush=True)
    start_time = time.time()
    response = ollama_client.generate_response(query)
    end_time = time.time()
    
    print(response)
    print(f"[Response time: {end_time - start_time:.2f}s]")
    
    # Streaming response test
    query = "Tell me about three interesting facts about Paris in a numbered list."
    print(f"\nStreaming Response Test:")
    print(f"Query: {query}")
    
    print("Response (streaming): ", end="", flush=True)
    start_time = time.time()
    last_response = ""
    
    for chunk, full_response in ollama_client.generate_streaming_response(query):
        print(chunk, end="", flush=True)
        last_response = full_response
        
    end_time = time.time()
    print(f"\n[Response time: {end_time - start_time:.2f}s]")
    
    # Interactive demo with streaming responses
    print("\n=== Interactive Streaming Demo ===")
    print("Type your questions and see the responses stream in real-time.")
    print("Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_input = get_user_input("\nYou: ")
        
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
        
        # Generate streaming response
        print("Assistant: ", end="", flush=True)
        start_time = time.time()
        complete_response = ""
        
        for chunk, full_response in ollama_client.generate_streaming_response_with_rag(
            user_input, conversation_history=conversation_history
        ):
            print(chunk, end="", flush=True)
            complete_response = full_response
            
        end_time = time.time()
        print(f"\n[Response time: {end_time - start_time:.2f}s]")
        
        # Add the complete response to memory
        memory.add_ai_message(complete_response)

def test_rag_streaming():
    """Test streaming responses with RAG for crime prediction queries."""
    print("\n=== Crime Prediction RAG Streaming Demo ===")
    
    # Initialize Ollama client
    ollama_client = OllamaClient()
    
    # Test crime query with streaming
    crime_query = "What's the crime risk at coordinates 41.8781, -87.6298 tonight at 10pm?"
    print(f"Query: {crime_query}")
    
    print("Response: ", end="", flush=True)
    start_time = time.time()
    complete_response = ""
    
    for chunk, full_response in ollama_client.generate_streaming_response_with_rag(crime_query):
        print(chunk, end="", flush=True)
        complete_response = full_response
        
    end_time = time.time()
    print(f"\n[Response time: {end_time - start_time:.2f}s]")
    
    # Test non-crime query with streaming
    general_query = "What's the weather like in Chicago?"
    print(f"\nQuery: {general_query}")
    
    print("Response: ", end="", flush=True)
    start_time = time.time()
    
    for chunk, full_response in ollama_client.generate_streaming_response_with_rag(general_query):
        print(chunk, end="", flush=True)
        
    end_time = time.time()
    print(f"\n[Response time: {end_time - start_time:.2f}s]")

if __name__ == "__main__":
    show_streaming_demo()
    test_rag_streaming() 