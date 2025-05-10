#!/usr/bin/env python3
"""
Test script for evaluating follow-up query handling in the crime prediction bot.
This script simulates a conversation with follow-up queries to check if the bot
maintains context properly.
"""
import os
import sys
import time

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm.ollama_client import OllamaClient
from src.memory.conversation import ConversationMemory

def test_follow_up_queries():
    """Test the chatbot's ability to handle follow-up queries."""
    # Initialize components
    print("Initializing Crime Prediction Bot for follow-up query testing...")
    ollama_client = OllamaClient()
    memory = ConversationMemory()
    
    # Add system message
    system_message = """
    You are a specialized crime prediction AI assistant. Your primary purpose is to analyze crime risk data 
    and provide objective safety assessments for specific locations and times.
    """
    memory.add_system_message(system_message)
    
    # Test scenarios with follow-up queries
    test_scenarios = [
        # Scenario 1: Follow-up changing time
        {
            "name": "Time Change Follow-up",
            "queries": [
                "What's the crime risk at coordinates 41.8781, -87.6298 on Thursday at 10pm?",
                "What about at 2am?",
                "And on Friday?"
            ]
        },
        # Scenario 2: Follow-up changing location
        {
            "name": "Location Change Follow-up",
            "queries": [
                "Is it safe at latitude 41.8781 and longitude -87.6298 tonight?",
                "What about at 41.7636, -87.5830?",
                "And downtown?"
            ]
        },
        # Scenario 3: Vague initial query followed by specifics
        {
            "name": "Vague to Specific Follow-up",
            "queries": [
                "How safe is downtown Chicago?",
                "What about at 41.8781, -87.6298 specifically?",
                "Is it better during the day?"
            ]
        },
        # Scenario 4: Multiple parameter changes
        {
            "name": "Multiple Parameter Changes",
            "queries": [
                "Crime risk at 41.8781, -87.6298 on Monday at 3pm?",
                "What about Wednesday night?",
                "And at 41.7636, -87.5830?"
            ]
        }
    ]
    
    # Test each scenario
    for i, scenario in enumerate(test_scenarios):
        print(f"\n\n{'='*50}")
        print(f"SCENARIO {i+1}: {scenario['name']}")
        print(f"{'='*50}")
        
        # Clear memory for each new scenario
        memory.clear()
        memory.add_system_message(system_message)
        
        # Process each query in the scenario
        for j, query in enumerate(scenario["queries"]):
            print(f"\nQUERY {j+1}: {query}")
            print("-" * 50)
            
            # Add query to memory
            memory.add_user_message(query)
            
            # Get conversation history
            conversation_history = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(), "content": msg.content}
                for msg in memory.get_messages()
            ]
            
            # Generate response
            print("Response: ", end="", flush=True)
            start_time = time.time()
            complete_response = ""
            
            for chunk, full_response in ollama_client.generate_streaming_response_with_rag(
                query, conversation_history=conversation_history
            ):
                print(chunk, end="", flush=True)
                complete_response = full_response
                
            # Add response to memory
            memory.add_ai_message(complete_response)
            
            # Print timing info
            end_time = time.time()
            print(f"\n[Response time: {end_time - start_time:.2f}s]")
            
            # Check if parameters were extracted properly
            query_processor = ollama_client.rag_manager.query_processor
            is_crime_query = query_processor.is_crime_prediction_query(query)
            params = query_processor.extract_parameters(query)
            
            print("\nQuery Analysis:")
            print(f"  Is crime query: {is_crime_query}")
            print(f"  Parameters extracted:")
            print(f"    - Date: {params.get('date')}")
            print(f"    - Time: {params.get('time')}")
            print(f"    - Coordinates: ({params.get('latitude')}, {params.get('longitude')})")
            print(f"  Current context:")
            print(f"    - Date: {query_processor.context.get('date')}")
            print(f"    - Time: {query_processor.context.get('time')}")
            print(f"    - Coordinates: ({query_processor.context.get('latitude')}, {query_processor.context.get('longitude')})")
            
            # Small delay between queries for clarity
            time.sleep(1)

def test_specific_follow_up():
    """Test with a specific follow-up query that might be tricky."""
    
    print("\n\n" + "="*50)
    print("TESTING SPECIFIC FOLLOW-UP SCENARIOS")
    print("="*50)
    
    # Initialize components
    ollama_client = OllamaClient()
    memory = ConversationMemory()
    
    # Add system message
    system_message = """
    You are a specialized crime prediction AI assistant. Your primary purpose is to analyze crime risk data 
    and provide objective safety assessments for specific locations and times.
    """
    memory.add_system_message(system_message)
    
    # Test specific tricky follow-ups
    queries = [
        "What's the crime risk at coordinates 41.8781, -87.6298 on Thursday at 10pm?",
        "What about Friday?",  # Day change only
        "Is it safer during the day?",  # Time change but vague
        "What's the risk level at the same place next week?",  # Relative time change
        "Should I be concerned about theft specifically?",  # Crime type specification
    ]
    
    for i, query in enumerate(queries):
        print(f"\nQUERY {i+1}: {query}")
        print("-" * 50)
        
        # Add query to memory
        memory.add_user_message(query)
        
        # Get conversation history
        conversation_history = [
            {"role": msg.__class__.__name__.replace("Message", "").lower(), "content": msg.content}
            for msg in memory.get_messages()
        ]
        
        # Generate response
        print("Response: ", end="", flush=True)
        complete_response = ""
        
        for chunk, full_response in ollama_client.generate_streaming_response_with_rag(
            query, conversation_history=conversation_history
        ):
            print(chunk, end="", flush=True)
            complete_response = full_response
            
        # Add response to memory
        memory.add_ai_message(complete_response)
        
        # Check context
        query_processor = ollama_client.rag_manager.query_processor
        params = query_processor.extract_parameters(query)
        
        print("\nQuery Analysis:")
        print(f"  Parameters extracted:")
        print(f"    - Date: {params.get('date')}")
        print(f"    - Time: {params.get('time')}")
        print(f"    - Coordinates: ({params.get('latitude')}, {params.get('longitude')})")
        print(f"  Current context:")
        print(f"    - Date: {query_processor.context.get('date')}")
        print(f"    - Time: {query_processor.context.get('time')}")
        print(f"    - Coordinates: ({query_processor.context.get('latitude')}, {query_processor.context.get('longitude')})")
        
        # Small delay between queries for clarity
        time.sleep(1)

if __name__ == "__main__":
    test_follow_up_queries()
    test_specific_follow_up() 