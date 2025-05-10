#!/usr/bin/env python3
"""
Test script for the RAG implementation with the crime prediction model.
This script tests the RAG manager's ability to process queries about crime risk.
"""
import sys
import os
import joblib
from datetime import datetime
import pandas as pd
import math

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the RAG manager and Query Processor
from src.retrieval.rag_manager import RAGManager
from src.retrieval.query_processor import CrimeQueryProcessor

def find_model_path():
    """Find the path to the crime prediction model."""
    possible_paths = [
        os.path.join(os.getcwd(), "crime_model.pkl"),
        os.path.join(os.getcwd(), "models", "crime_model.pkl"),
        os.path.join(os.getcwd(), "data", "models", "crime_model.pkl")
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            print(f"Found crime model at: {path}")
            break
    
    if model_path is None:
        print("ERROR: Could not find crime_model.pkl in any of the expected locations.")
        print("Please ensure the model file exists in one of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        sys.exit(1)
    
    return model_path

def test_process_query():
    """Test the RAG manager's query processing capabilities."""
    model_path = find_model_path()
    
    # Initialize RAG manager with correct model path
    config = {
        "model": {
            "crime_model_path": model_path
        }
    }
    rag_manager = RAGManager(config)
    
    # Also initialize a query processor directly for parameter extraction
    query_processor = CrimeQueryProcessor()
    
    # Test queries
    test_queries = [
        "What's the crime risk in Chicago on January 1, 2025?",
        "Is it safe to visit downtown Chicago (41.87917, -87.62954) on New Year's Eve at midnight?",
        "Tell me about the crime statistics at coordinates 41.97974, -87.76932 on January 30, 2025 at noon",
        "What's the crime risk at 41.80713, -87.74314 on September 8, 2024?",
        "Should I be worried about crime at latitude 41.85112 and longitude -87.62766 on Christmas 2024?",
    ]
    
    print("Testing RAG implementation with sample queries...")
    print("-" * 50)
    
    for i, query in enumerate(test_queries):
        print(f"Test {i+1} - Query: \"{query}\"")
        
        # Process query with RAG manager
        try:
            # First check if this is a crime query
            is_crime_query = query_processor.is_crime_prediction_query(query)
            print(f"  Is crime query: {is_crime_query}")
            
            # Extract parameters using the query processor
            params = query_processor.extract_parameters(query)
            print(f"  Extracted parameters: {params}")
            
            # Process the query through the RAG manager
            is_rag_query, rag_result = rag_manager.process_query(query)
            
            if is_rag_query and rag_result:
                print(f"  RAG query: Yes")
                print(f"  Complete parameters: {rag_result.get('complete', False)}")
                
                if rag_result.get('complete', False):
                    print(f"  Probability: {rag_result.get('probability', 'N/A'):.4f}")
                    
                    # Get the LLM-formatted response
                    formatted = rag_manager.format_for_llm(rag_result)
                    if len(formatted) > 150:
                        print(f"  Formatted for LLM: {formatted[:150]}...")
                    else:
                        print(f"  Formatted for LLM: {formatted}")
                else:
                    if 'follow_up' in rag_result:
                        print(f"  Missing info: {', '.join(rag_result['follow_up'].get('missing_info', []))}")
                        print(f"  Follow-up: {rag_result['follow_up'].get('question', 'N/A')}")
            else:
                print("  Not processed as a RAG query")
            
            # If we have the parameters, test a direct prediction
            if params and all(k in params for k in ['date', 'time', 'longitude', 'latitude']):
                print("  Testing direct prediction with correct feature format...")
                model = joblib.load(model_path)
                
                # Create features in the correct format
                date_obj = datetime.strptime(f"{params['date']} {params['time']}", '%Y-%m-%d %H:%M')
                lat = float(params['latitude'])
                lng = float(params['longitude'])
                
                # Prepare features for the model based on diagnostic results
                cos_hour, sin_hour, cos_weekday, sin_weekday = encode_time_features(date_obj)
                features = pd.DataFrame([{
                    'Latitude': lat,
                    'Longitude': lng,
                    'sin_hour': sin_hour,
                    'cos_hour': cos_hour,
                    'sin_weekday': sin_weekday,
                    'cos_weekday': cos_weekday
                }])
                
                # Get prediction using proper feature format
                probability = model.predict_proba(features)[0][1]
                
                print(f"  Direct prediction: {probability:.4f} ({'High' if probability > 0.5 else 'Low'} risk)")
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    print("RAG implementation testing complete!")

def encode_time_features(date_obj):
    """Encode time features for model input."""
    # Hour features (0-23 hours) - circular encoding
    hour = date_obj.hour + date_obj.minute/60.0
    cos_hour = math.cos(2 * math.pi * hour / 24.0)
    sin_hour = math.sin(2 * math.pi * hour / 24.0)
    
    # Weekday features (0-6, where 0 is Monday)
    weekday = date_obj.weekday()
    cos_weekday = math.cos(2 * math.pi * weekday / 7.0)
    sin_weekday = math.sin(2 * math.pi * weekday / 7.0)
    
    return cos_hour, sin_hour, cos_weekday, sin_weekday

def test_interactive():
    """Interactive testing of the RAG implementation."""
    model_path = find_model_path()
    
    # Initialize RAG manager
    config = {
        "model": {
            "crime_model_path": model_path
        }
    }
    rag_manager = RAGManager(config)
    
    # Initialize query processor directly for parameter extraction
    query_processor = CrimeQueryProcessor()
    
    print("Interactive RAG Implementation Testing")
    print("-" * 50)
    print("Enter 'q' to exit")
    
    while True:
        try:
            # Get user input
            query = input("\nEnter your query: ")
            if query.lower() == 'q':
                break
            
            # Process query with RAG manager
            is_crime_query = query_processor.is_crime_prediction_query(query)
            print(f"Is crime query: {is_crime_query}")
            
            # Extract parameters using the query processor
            params = query_processor.extract_parameters(query)
            print(f"Extracted parameters: {params}")
            
            # Process the query through the RAG manager
            is_rag_query, rag_result = rag_manager.process_query(query)
            
            if is_rag_query and rag_result:
                print(f"RAG query: Yes")
                print(f"Complete parameters: {rag_result.get('complete', False)}")
                
                if rag_result.get('complete', False):
                    print(f"Probability: {rag_result.get('probability', 'N/A'):.4f}")
                    
                    # Get the LLM-formatted response
                    formatted = rag_manager.format_for_llm(rag_result)
                    print(f"Formatted for LLM: {formatted}")
                else:
                    if 'follow_up' in rag_result:
                        print(f"Missing info: {', '.join(rag_result['follow_up'].get('missing_info', []))}")
                        print(f"Follow-up: {rag_result['follow_up'].get('question', 'N/A')}")
            else:
                print("Not processed as a RAG query")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("Interactive testing complete!")

if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        test_interactive()
    else:
        test_process_query() 