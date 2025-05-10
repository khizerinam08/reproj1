"""
Test script for the crime prediction model RAG system.

This script tests the Crime Model RAG implementation by processing
sample queries and displaying predictions.
"""
import os
import sys
import random
from datetime import datetime, timedelta

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import the RAG classes
from src.retrieval.crime_model_rag import CrimeModelRAG
from src.retrieval.query_processor import CrimeQueryProcessor

def test_query_processor():
    """Test the query processor with sample queries."""
    print("\n===== Testing Query Processor =====")
    processor = CrimeQueryProcessor()
    
    test_queries = [
        "What is the probability of crime at latitude 41.8781 and longitude -87.6298 tomorrow at 3pm?",
        "Is it safe to walk around downtown at night?",
        "What's the crime risk on Friday evening at 41.8781, -87.6298?",
        "How likely is a robbery in Chicago at noon on Monday?",
        "What's the risk of crime on December 25th at midnight?",
        "Should I be worried about safety at coordinates 41.7, -87.5 on Sunday morning?",
        "Explain the crime model to me",  # Not a crime prediction query
        "Tell me about the crime trends in Chicago"  # Not a specific prediction query
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Check if this is a crime prediction query
        is_crime_query = processor.is_crime_prediction_query(query)
        print(f"Is crime prediction query: {is_crime_query}")
        
        if is_crime_query:
            # Extract parameters
            params = processor.extract_parameters(query)
            print(f"Extracted parameters: {params}")
        else:
            print("Not a crime prediction query - parameters not extracted")

def test_crime_model_prediction():
    """Test the crime model with sample data."""
    print("\n===== Testing Crime Model Prediction =====")
    
    # Path to the model file
    model_path = os.path.join(project_dir, "crime_model.pkl")
    
    # Initialize the RAG model
    try:
        crime_rag = CrimeModelRAG(model_path)
        print("Successfully loaded the crime model")
    except Exception as e:
        print(f"Error loading the crime model: {e}")
        return
    
    # Generate some test cases
    test_cases = []
    
    # Current date/time
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    
    # Sample coordinates (Chicago area)
    chicago_coords = [
        (-87.6298, 41.8781),  # Downtown Chicago
        (-87.6691, 41.9742),  # Rogers Park
        (-87.6846, 41.7376),  # Chicago Lawn
        (-87.7162, 41.8520),  # Pilsen
        (-87.5830, 41.7636)   # South Shore
    ]
    
    # Generate test cases with different times/dates
    for i in range(5):
        # Pick random coordinates
        lng, lat = random.choice(chicago_coords)
        
        # Use different times
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        
        # Use different dates
        date_offset = random.randint(0, 7)
        test_date = (now + timedelta(days=date_offset)).strftime("%Y-%m-%d")
        
        test_cases.append((test_date, time_str, lng, lat))
    
    # Add specific test cases
    test_cases.append((today, "23:00", -87.6298, 41.8781))  # Downtown at night
    test_cases.append((today, "12:00", -87.6298, 41.8781))  # Downtown at noon
    
    # Run test cases
    for date_str, time_str, lng, lat in test_cases:
        try:
            # Make prediction
            prob = crime_rag.predict_crime_probability(date_str, time_str, lng, lat)
            
            # Generate explanation
            params = {
                'date': date_str,
                'time': time_str,
                'longitude': lng,
                'latitude': lat
            }
            explanation = crime_rag.generate_explanation(prob, params)
            
            print(f"\nPrediction for {date_str} at {time_str}, location ({lat}, {lng}):")
            print(f"Probability: {prob:.4f}")
            print(f"Explanation: {explanation}")
        except Exception as e:
            print(f"Error making prediction: {e}")

def test_end_to_end():
    """Test the entire pipeline from query to prediction."""
    print("\n===== Testing End-to-End Pipeline =====")
    
    # Path to the model file
    model_path = os.path.join(project_dir, "crime_model.pkl")
    
    # Initialize the components
    try:
        crime_rag = CrimeModelRAG(model_path)
        processor = CrimeQueryProcessor()
    except Exception as e:
        print(f"Error initializing components: {e}")
        return
    
    # Sample queries
    test_queries = [
        "What's the probability of crime in downtown Chicago (41.8781, -87.6298) tonight at 10pm?",
        "How safe is it to walk around at latitude 41.8781 and longitude -87.6298 tomorrow afternoon?",
        "What's the crime risk on Saturday evening at coordinates 41.7376, -87.6846?",
        "Is it dangerous in South Shore (41.7636, -87.5830) at midnight?",
        "Should I be worried about safety at 41.9742, -87.6691 on Sunday morning at 8am?"
    ]
    
    for query in test_queries:
        print(f"\nOriginal query: '{query}'")
        
        # Check if this is a crime prediction query
        is_crime_query = processor.is_crime_prediction_query(query)
        print(f"Is crime prediction query: {is_crime_query}")
        
        if is_crime_query:
            # Extract parameters
            params = processor.extract_parameters(query)
            print(f"Extracted parameters: {params}")
            
            # If parameters are complete, make prediction
            if params.get('complete', False):
                try:
                    # Make prediction
                    prob = crime_rag.predict_crime_probability(
                        params['date'], params['time'], 
                        params['longitude'], params['latitude']
                    )
                    
                    # Generate explanation
                    explanation = crime_rag.generate_explanation(prob, params)
                    
                    print(f"Crime prediction:")
                    print(f"Probability: {prob:.4f}")
                    print(f"Explanation: {explanation}")
                    
                    # Simulate LLM response formatting
                    llm_response = (
                        f"Based on the crime prediction model, {explanation} "
                        f"This prediction is based on historical crime data and time/location patterns."
                    )
                    print(f"\nSimulated LLM response: '{llm_response}'")
                except Exception as e:
                    print(f"Error making prediction: {e}")
            else:
                print("Incomplete parameters - would ask for clarification")
                
                # Simulate LLM asking for clarification
                missing_info = []
                if not params.get('date'):
                    missing_info.append("date")
                if not params.get('time'):
                    missing_info.append("time")
                if not (params.get('longitude') and params.get('latitude')):
                    missing_info.append("location coordinates")
                
                clarification = f"I need more information to predict crime risk. Could you provide: {', '.join(missing_info)}?"
                print(f"LLM clarification: '{clarification}'")
        else:
            print("Not a crime prediction query - would use regular LLM response")
            
            # Simulate standard LLM response
            standard_response = "I don't have specific crime prediction data for that query. I can provide general safety tips instead."
            print(f"Standard LLM response: '{standard_response}'")

if __name__ == "__main__":
    # Test the query processor
    test_query_processor()
    
    # Test the crime model prediction
    test_crime_model_prediction()
    
    # Test the end-to-end pipeline
    test_end_to_end() 