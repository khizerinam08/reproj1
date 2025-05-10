#!/usr/bin/env python3
"""
Diagnostic script to examine the crime prediction model.
This script inspects the model's structure, features, and makes test predictions
to understand why it's not returning expected probabilities.
"""
import sys
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import math

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

def main():
    """Run diagnostic tests on the crime prediction model."""
    model_path = find_model_path()
    
    print("\nLoading model...")
    model = joblib.load(model_path)
    
    print("\nModel Information:")
    print(f"Type: {type(model)}")
    
    # Check if it's a scikit-learn model
    if hasattr(model, 'feature_names_in_'):
        print(f"Feature names: {model.feature_names_in_}")
    
    if hasattr(model, 'classes_'):
        print(f"Classes: {model.classes_}")
    
    if hasattr(model, 'n_features_in_'):
        print(f"Number of features: {model.n_features_in_}")
    
    if hasattr(model, 'n_estimators'):
        print(f"Number of estimators: {model.n_estimators}")
    
    # Try test predictions with data in different formats
    print("\nTest predictions:")
    
    # Sample data from your dataset
    sample_data = [
        {"date": "2024-06-06", "coordinates": (41.70804, -87.64834), "label": 0},
        {"date": "2024-09-08", "coordinates": (41.80713, -87.74314), "label": 1},
    ]
    
    for i, data in enumerate(sample_data):
        print(f"\nSample {i+1}:")
        date_str = data['date']
        lat, lng = data['coordinates']
        
        # Convert to datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Test for different times
        for hour in [0, 12]:
            date_obj = date_obj.replace(hour=hour)
            cos_hour, sin_hour, cos_weekday, sin_weekday = encode_time_features(date_obj)
            
            # Try different feature formats
            # Format 1: Standard array with expected order (based on most sklearn models)
            features_array = np.array([[cos_hour, sin_hour, cos_weekday, sin_weekday, lng, lat]])
            print(f"\n  Time: {hour}:00")
            
            try:
                prob = model.predict_proba(features_array)[0][1]
                print(f"  Format 1 probability: {prob:.4f}")
            except Exception as e:
                print(f"  Format 1 error: {e}")
            
            # Format 2: Using feature names if available
            if hasattr(model, 'feature_names_in_'):
                try:
                    feature_dict = {}
                    for i, name in enumerate(model.feature_names_in_):
                        if 'cos_hour' in name or name == 'cos_hour':
                            feature_dict[name] = cos_hour
                        elif 'sin_hour' in name or name == 'sin_hour':
                            feature_dict[name] = sin_hour
                        elif 'cos_weekday' in name or name == 'cos_weekday':
                            feature_dict[name] = cos_weekday
                        elif 'sin_weekday' in name or name == 'sin_weekday':
                            feature_dict[name] = sin_weekday
                        elif 'lat' in name.lower() or name == 'Latitude':
                            feature_dict[name] = lat
                        elif 'lon' in name.lower() or name == 'Longitude':
                            feature_dict[name] = lng
                        else:
                            feature_dict[name] = 0.0  # Default for unknown features
                            
                    feature_df = pd.DataFrame([feature_dict])
                    prob = model.predict_proba(feature_df)[0][1]
                    print(f"  Format 2 probability: {prob:.4f}")
                except Exception as e:
                    print(f"  Format 2 error: {e}")
            
            # Format 3: Try reverse order of features
            features_array_rev = np.array([[lat, lng, cos_weekday, sin_weekday, cos_hour, sin_hour]])
            try:
                prob = model.predict_proba(features_array_rev)[0][1]
                print(f"  Format 3 probability: {prob:.4f}")
            except Exception as e:
                print(f"  Format 3 error: {e}")
            
            # Format 4: Try only the time features
            features_time = np.array([[cos_hour, sin_hour, cos_weekday, sin_weekday]])
            try:
                prob = model.predict_proba(features_time)[0][1]
                print(f"  Format 4 probability: {prob:.4f}")
            except Exception as e:
                print(f"  Format 4 error: {e}")
                
            # Format 5: Try only the coordinates
            features_coords = np.array([[lng, lat]])
            try:
                prob = model.predict_proba(features_coords)[0][1]
                print(f"  Format 5 probability: {prob:.4f}")
            except Exception as e:
                print(f"  Format 5 error: {e}")
    
    # Check the importances if available
    if hasattr(model, 'feature_importances_'):
        print("\nFeature importances:")
        importances = model.feature_importances_
        if hasattr(model, 'feature_names_in_'):
            for name, importance in zip(model.feature_names_in_, importances):
                print(f"  {name}: {importance:.4f}")
        else:
            for i, importance in enumerate(importances):
                print(f"  Feature {i}: {importance:.4f}")
    
    print("\nDiagnostic complete!")

if __name__ == "__main__":
    main() 