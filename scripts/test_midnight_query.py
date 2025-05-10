#!/usr/bin/env python3
"""
Test script to check if midnight queries and correct feature ordering are working.
This specifically tests the bugfix for the issue where 12am queries weren't returning high risk.
"""
import sys
import os
import joblib
from datetime import datetime
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary components
from src.retrieval.crime_model_rag import CrimeModelRAG
from src.retrieval.query_processor import CrimeQueryProcessor

def test_midnight_query():
    """Test a midnight query directly against the CrimeModelRAG class."""
    print("\n=== Testing Midnight Query with CrimeModelRAG ===")
    
    # Find the model path
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
        print("ERROR: Could not find crime_model.pkl")
        sys.exit(1)
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Test coordinates from the example
    latitude = 41.70931
    longitude = -87.66719
    
    # Test with midnight
    date_str = "2023-11-02"  # Thursday
    time_str = "00:00"  # Midnight
    
    print(f"\nTesting coordinates ({longitude}, {latitude}) on {date_str} at {time_str}")
    
    # Get features from preprocess_query
    features = crime_model.preprocess_query(date_str, time_str, longitude, latitude)
    print(f"Features shape: {features.shape}")
    print(f"Features columns: {features.columns.tolist()}")
    print(f"Features values: \n{features}")
    
    # Get prediction
    probability = crime_model.predict_crime_probability(date_str, time_str, longitude, latitude)
    print(f"Probability: {probability:.4f} ({'High' if probability > 0.5 else 'Low'} risk)")
    
    # Generate explanation
    query_params = {
        'date': date_str,
        'time': time_str,
        'longitude': longitude,
        'latitude': latitude
    }
    explanation = crime_model.generate_explanation(probability, query_params)
    print(f"Explanation: {explanation}")
    
    # Test alternative midnight formats
    time_formats = [
        "00:00",      # 24-hour format
        "12:00 AM",   # 12-hour format with space
        "12AM",       # 12-hour format without space
        "12am",       # lowercase
        "midnight"    # word
    ]
    
    print("\n=== Testing Different Midnight Formats ===")
    for time_format in time_formats:
        print(f"\nTesting with time format: '{time_format}'")
        
        # Parse using query processor
        processor = CrimeQueryProcessor()
        query = f"What's the crime risk at {longitude},{latitude} on Thursday at {time_format}?"
        extracted_time = processor.extract_time(query)
        
        print(f"Extracted time: {extracted_time}")
        if extracted_time == "00:00":
            print("✓ Time extraction CORRECT")
        else:
            print("✗ Time extraction INCORRECT")
        
        # Get full parameters
        params = processor.extract_parameters(query)
        print(f"Extracted parameters: {params}")
        
        # Get prediction
        probability = crime_model.predict_crime_probability(
            params['date'], params['time'], params['longitude'], params['latitude']
        )
        print(f"Probability: {probability:.4f} ({'High' if probability > 0.5 else 'Low'} risk)")

if __name__ == "__main__":
    test_midnight_query() 