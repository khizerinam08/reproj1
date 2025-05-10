"""
Script to preprocess data for the crime prediction model.

This script demonstrates how to preprocess data into the format expected
by the crime prediction model.
"""
import pandas as pd
import numpy as np
import math
from datetime import datetime
import os
import sys

def preprocess_crime_data(data_path):
    """
    Preprocess crime data into the format expected by the model.
    
    Args:
        data_path: Path to the input data CSV file
        
    Returns:
        Processed DataFrame with features in the expected format
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    print(f"Original data shape: {df.shape}")
    print(f"Original columns: {df.columns.tolist()}")
    
    # Check if data already has the expected columns
    expected_columns = ['date', 'cos_hour', 'sin_hour', 'cos_weekday', 
                        'sin_weekday', 'Longitude', 'Latitude', 'label']
    
    if set(expected_columns).issubset(set(df.columns)):
        print("Data already has the expected format")
        return df
    
    # Preprocess data if it doesn't have the expected format
    print("Preprocessing data...")
    
    # Process date/time columns (assuming 'Date' and 'Time' columns exist)
    if 'Date' in df.columns and 'Time' in df.columns:
        # Combine date and time
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        
        # Extract hour and convert to radians for circular encoding
        df['Hour'] = df['DateTime'].dt.hour + df['DateTime'].dt.minute/60.0
        df['cos_hour'] = np.cos(2 * np.pi * df['Hour'] / 24.0)
        df['sin_hour'] = np.sin(2 * np.pi * df['Hour'] / 24.0)
        
        # Extract weekday and convert to radians for circular encoding
        df['Weekday'] = df['DateTime'].dt.weekday
        df['cos_weekday'] = np.cos(2 * np.pi * df['Weekday'] / 7.0)
        df['sin_weekday'] = np.sin(2 * np.pi * df['Weekday'] / 7.0)
        
        # Create date column in YYYY-MM-DD format
        df['date'] = df['DateTime'].dt.strftime('%Y-%m-%d')
    else:
        print("Warning: Date/Time columns not found, assuming separate features provided")
    
    # Check for coordinates
    if 'Longitude' not in df.columns or 'Latitude' not in df.columns:
        print("Warning: Coordinate columns not found")
        
    # Check for label
    if 'label' not in df.columns and 'CrimeType' in df.columns:
        print("Converting crime type to binary label")
        # This would need to be customized based on your classification scheme
        df['label'] = (df['CrimeType'] != 'None').astype(int)
    
    # Select only the required columns
    required_columns = [col for col in expected_columns if col in df.columns]
    df_processed = df[required_columns]
    
    print(f"Processed data shape: {df_processed.shape}")
    print(f"Processed columns: {df_processed.columns.tolist()}")
    
    return df_processed

def convert_single_entry(date_str, time_str, longitude, latitude):
    """
    Convert a single data point to the format expected by the model.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        time_str: Time string in HH:MM format
        longitude: Longitude coordinate
        latitude: Latitude coordinate
        
    Returns:
        Dictionary with processed features
    """
    # Parse date and time
    date_format = "%Y-%m-%d"
    time_format = "%H:%M"
    date_obj = datetime.strptime(date_str, date_format)
    time_obj = datetime.strptime(time_str, time_format)
    
    # Combine date and time
    date_time = datetime.combine(date_obj.date(), time_obj.time())
    
    # Extract hour and convert to radians for circular encoding
    hour = date_time.hour + date_time.minute/60.0
    cos_hour = math.cos(2 * math.pi * hour / 24.0)
    sin_hour = math.sin(2 * math.pi * hour / 24.0)
    
    # Extract weekday and convert to radians for circular encoding
    weekday = date_time.weekday()
    cos_weekday = math.cos(2 * math.pi * weekday / 7.0)
    sin_weekday = math.sin(2 * math.pi * weekday / 7.0)
    
    # Create feature dictionary
    features = {
        'date': date_str,
        'cos_hour': cos_hour,
        'sin_hour': sin_hour,
        'cos_weekday': cos_weekday,
        'sin_weekday': sin_weekday,
        'Longitude': longitude,
        'Latitude': latitude
    }
    
    return features

def create_sample_data(output_path, num_samples=100):
    """
    Create sample data for testing the model.
    
    Args:
        output_path: Path to save the sample data
        num_samples: Number of samples to generate
    """
    print(f"Generating {num_samples} sample data points...")
    
    # Generate random data
    data = []
    
    for _ in range(num_samples):
        # Random date in 2023
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)  # Simplify to avoid month length issues
        date_str = f"2023-{month:02d}-{day:02d}"
        
        # Random time
        hour = np.random.randint(0, 24)
        minute = np.random.randint(0, 60)
        time_str = f"{hour:02d}:{minute:02d}"
        
        # Random coordinates in Chicago area
        longitude = np.random.uniform(-87.7, -87.5)
        latitude = np.random.uniform(41.7, 42.0)
        
        # Process features
        features = convert_single_entry(date_str, time_str, longitude, latitude)
        
        # Add a random label
        features['label'] = np.random.randint(0, 2)
        
        data.append(features)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Sample data saved to {output_path}")
    
    return df

if __name__ == "__main__":
    # Get the absolute path to the project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Paths for data
    raw_data_dir = os.path.join(project_dir, "data", "raw")
    processed_data_dir = os.path.join(project_dir, "data", "processed")
    
    # Create directories if they don't exist
    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)
    
    # Path for sample data
    sample_data_path = os.path.join(raw_data_dir, "sample_crime_data.csv")
    
    # Create sample data for testing
    sample_df = create_sample_data(sample_data_path, num_samples=1000)
    
    # Preprocess the sample data
    processed_df = preprocess_crime_data(sample_data_path)
    
    # Save processed data
    processed_path = os.path.join(processed_data_dir, "processed_crime_data.csv")
    processed_df.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path}")
    
    # Example of converting a single entry
    print("\nExample of converting a single entry:")
    sample_entry = convert_single_entry("2023-03-15", "14:30", -87.6298, 41.8781)
    print(sample_entry) 