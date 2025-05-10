#!/usr/bin/env python3
"""
Test script for the crime prediction model.
This script tests the model's ability to predict crime incidents.
"""
import sys
import os
import joblib
from datetime import datetime
import numpy as np
import math
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

def prepare_features(date_obj, lat, lng):
    """
    Prepare features for the model in the correct format.
    Based on diagnostic results, the model expects features in this order:
    ['Latitude', 'Longitude', 'sin_hour', 'cos_hour', 'sin_weekday', 'cos_weekday']
    """
    cos_hour, sin_hour, cos_weekday, sin_weekday = encode_time_features(date_obj)
    
    # Create a DataFrame with named features matching the model's expectations
    features = {
        'Latitude': lat,
        'Longitude': lng,
        'sin_hour': sin_hour,
        'cos_hour': cos_hour,
        'sin_weekday': sin_weekday,
        'cos_weekday': cos_weekday
    }
    
    return pd.DataFrame([features])

def test_model_with_data(model, test_cases):
    """Test the model with various data points."""
    print("Testing crime prediction model...")
    
    for i, test_case in enumerate(test_cases):
        date_str = test_case['date']
        time_str = test_case['time']
        datetime_str = f"{date_str} {time_str}"
        coords = test_case['coordinates']
        expected_label = test_case['label']
        
        # Parse datetime
        date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        # Prepare features in the correct format
        features = prepare_features(date_obj, coords[0], coords[1])
        
        # Get prediction
        prob = model.predict_proba(features)[0][1]
        prediction = "High risk" if prob > 0.5 else "Low risk"
        
        # Print results
        print(f"Test {i+1} - {date_str} {time_str} at {coords}:")
        print(f"  Probability: {prob:.4f} ({prediction})")
        print(f"  Expected label: {expected_label}")
        
        # Generate a human-readable explanation
        time_description = "morning" if date_obj.hour < 12 else "afternoon" if date_obj.hour < 18 else "evening"
        print(f"  For the location at coordinates {coords[0]:.4f}, {coords[1]:.4f} on {date_str} at {time_str}, "
              f"the model predicts a {'high' if prob > 0.5 else 'low'} risk of crime with a probability of {prob*100:.1f}%.")
        print()

def main():
    """Run the crime model test."""
    model_path = find_model_path()
    
    try:
        model = joblib.load(model_path)
        print(f"Successfully loaded model: {type(model).__name__}")
        
        # Test cases with various timestamps and coordinates
        test_cases = [
            {"date": "2024-06-06", "time": "12:00", "coordinates": (41.70804, -87.64834), "label": 0},
            {"date": "2024-06-06", "time": "00:00", "coordinates": (41.70804, -87.64834), "label": 0},
            {"date": "2024-09-08", "time": "12:00", "coordinates": (41.80713, -87.74314), "label": 1},
            {"date": "2024-09-08", "time": "00:00", "coordinates": (41.80713, -87.74314), "label": 1},
            {"date": "2024-12-25", "time": "12:00", "coordinates": (41.85112, -87.62766), "label": 0},
            {"date": "2024-12-25", "time": "00:00", "coordinates": (41.85112, -87.62766), "label": 0},
            {"date": "2025-01-01", "time": "00:00", "coordinates": (41.87917, -87.62954), "label": 1},
            {"date": "2025-01-01", "time": "12:00", "coordinates": (41.87917, -87.62954), "label": 1},
            {"date": "2025-01-30", "time": "12:00", "coordinates": (41.97974, -87.76932), "label": 0},
            {"date": "2025-01-30", "time": "18:00", "coordinates": (41.97974, -87.76932), "label": 0},
        ]
        
        test_model_with_data(model, test_cases)
        
        # Interactive mode if requested
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            print("\nEntering interactive mode. Enter 'q' to quit.")
            while True:
                try:
                    date_input = input("\nEnter date (YYYY-MM-DD): ")
                    if date_input.lower() == 'q':
                        break
                    
                    time_input = input("Enter time (HH:MM): ")
                    if time_input.lower() == 'q':
                        break
                    
                    lat_input = input("Enter latitude: ")
                    if lat_input.lower() == 'q':
                        break
                    
                    lng_input = input("Enter longitude: ")
                    if lng_input.lower() == 'q':
                        break
                    
                    date_obj = datetime.strptime(f"{date_input} {time_input}", '%Y-%m-%d %H:%M')
                    lat = float(lat_input)
                    lng = float(lng_input)
                    
                    features = prepare_features(date_obj, lat, lng)
                    prob = model.predict_proba(features)[0][1]
                    prediction = "High risk" if prob > 0.5 else "Low risk"
                    
                    print(f"\nPrediction for {date_input} {time_input} at ({lat}, {lng}):")
                    print(f"  Probability: {prob:.4f} ({prediction})")
                    print(f"  The model predicts a {'high' if prob > 0.5 else 'low'} risk of crime with a probability of {prob*100:.1f}%.")
                    
                except Exception as e:
                    print(f"Error: {e}")
        
        print("\nModel testing complete!")
        
    except Exception as e:
        print(f"Error loading or testing the model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 