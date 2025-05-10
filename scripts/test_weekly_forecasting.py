#!/usr/bin/env python3
"""
Test script for weekly crime probability forecasting functionality.
This script demonstrates the batch prediction capabilities for generating
crime probability forecasts across an entire week.
"""
import os
import sys
import time
from datetime import datetime, timedelta

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval.crime_model_rag import CrimeModelRAG

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
            
    print("ERROR: Could not find crime_model.pkl")
    print("Please place a crime_model.pkl file in one of these locations:")
    for path in possible_paths:
        print(f"- {path}")
    sys.exit(1)

def test_handle_default_coordinates():
    """Test the system's handling of default coordinates."""
    print("\n" + "="*80)
    print("Testing Default Coordinates Handling")
    print("="*80)
    
    # Find the model path
    model_path = find_model_path()
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Create test parameters with default coordinates flag
    test_params = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "10:00",
        "longitude": -87.6298, 
        "latitude": 41.8781,
        "using_default": True
    }
    
    # Test explanation generation
    explanation = crime_model.generate_explanation(0.5, test_params)
    
    print("Testing explanation with default coordinates:")
    print("-" * 50)
    print(explanation)
    print("-" * 50)
    
    # Verify the explanation mentions the need for a location
    if "didn't specify a location" in explanation:
        print("✅ Default coordinates correctly detected and handled")
    else:
        print("❌ Failed to properly handle default coordinates")

def test_weekly_forecast():
    """Test the weekly crime probability forecasting functionality."""
    print("\n" + "="*80)
    print("Testing Weekly Crime Probability Forecasting")
    print("="*80)
    
    # Find the model path
    model_path = find_model_path()
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Define test locations
    test_locations = [
        ("Downtown Chicago", 41.87917, -87.62954),
        ("North Side Chicago", 41.97974, -87.76932),
        ("South Side Chicago", 41.80713, -87.74314)
    ]
    
    # Generate a start date for next week
    today = datetime.now()
    next_monday = today + timedelta(days=(7 - today.weekday()))
    start_date = next_monday.strftime("%Y-%m-%d")
    
    # Test for each location
    for location_name, latitude, longitude in test_locations:
        print(f"\nLocation: {location_name} ({latitude}, {longitude})")
        print("-" * 50)
        
        # Time the prediction
        start_time = time.time()
        
        # Generate weekly forecast
        weekly_forecast = crime_model.predict_weekly_crime_probabilities(
            start_date_str=start_date,
            longitude=longitude,
            latitude=latitude,
            hour_interval=6  # Every 6 hours to reduce output volume
        )
        
        end_time = time.time()
        print(f"Prediction time: {end_time - start_time:.2f} seconds")
        
        # Format the forecast
        formatted_forecast = crime_model.format_weekly_prediction(weekly_forecast)
        
        # Print the formatted forecast
        print("\n" + formatted_forecast)
        
        # Brief analysis
        print("\nData Analysis:")
        print(f"- Total time points: {len(weekly_forecast['probabilities'])}")
        print(f"- Average probability: {weekly_forecast['summary']['avg_probability']:.2%}")
        
        # Print daily summary
        print("\nProbability by day (avg):")
        for day, stats in weekly_forecast['daily_summary'].items():
            print(f"- {day}: {stats['avg']:.2%}")
        
        # Check cache performance - this should be much faster
        print("\nTesting cache performance...")
        cache_start_time = time.time()
        cached_forecast = crime_model.predict_weekly_crime_probabilities(
            start_date_str=start_date,
            longitude=longitude,
            latitude=latitude,
            hour_interval=6
        )
        cache_end_time = time.time()
        
        print(f"Cached prediction time: {cache_end_time - cache_start_time:.2f} seconds")
        
        # Verify the cache is working
        if cache_end_time - cache_start_time < (end_time - start_time) / 10:
            print("✅ Cache is working effectively")
        else:
            print("❌ Cache may not be working properly")
        
        print("-" * 50)

def test_weekly_forecast_integration():
    """Test the integration with the RAG system."""
    print("\n" + "="*80)
    print("Testing Weekly Forecast Integration")
    print("="*80)
    
    # Find the model path
    model_path = find_model_path()
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Define test location
    latitude = 41.87917
    longitude = -87.62954
    
    # Generate a start date for this week
    today = datetime.now()
    this_week_start = today - timedelta(days=today.weekday())
    start_date = this_week_start.strftime("%Y-%m-%d")
    
    # Test different hour intervals
    for hour_interval in [3, 6, 12]:
        print(f"\nTesting with {hour_interval}-hour intervals")
        print("-" * 50)
        
        weekly_forecast = crime_model.predict_weekly_crime_probabilities(
            start_date_str=start_date,
            longitude=longitude,
            latitude=latitude,
            hour_interval=hour_interval
        )
        
        # Print summary statistics
        print(f"Total predictions: {weekly_forecast['metadata']['total_samples']}")
        print(f"Average probability: {weekly_forecast['summary']['avg_probability']:.2%}")
        print(f"Range: {weekly_forecast['summary']['min_probability']:.2%} to {weekly_forecast['summary']['max_probability']:.2%}")
        
        # Check that we have the expected number of points
        expected_points = (24 // hour_interval) * 7
        if weekly_forecast['metadata']['total_samples'] == expected_points:
            print(f"✅ Correct number of time points ({expected_points})")
        else:
            print(f"❌ Unexpected number of time points: {weekly_forecast['metadata']['total_samples']} (expected {expected_points})")
        
    print("-" * 50)
    print("Weekly forecast integration test complete")

def test_specific_hour_forecast():
    """Test the specific hour parameter for weekly forecasts."""
    print("\n" + "="*80)
    print("Testing Specific Hour Forecasting")
    print("="*80)
    
    # Find the model path
    model_path = find_model_path()
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Define test location
    location_name = "Downtown Chicago"
    latitude = 41.87917
    longitude = -87.62954
    
    # Generate a start date for this week
    today = datetime.now()
    this_week_start = today - timedelta(days=today.weekday())
    start_date = this_week_start.strftime("%Y-%m-%d")
    
    # Test specific hours (9am, 12pm, 6pm, 12am)
    test_hours = [9, 12, 18, 0]
    
    for hour in test_hours:
        # Format hour for display
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        am_pm = "AM" if hour < 12 else "PM"
        hour_display = f"{hour_12}{am_pm}"
        
        print(f"\nTesting specific hour: {hour_display}")
        print("-" * 50)
        
        # Time the prediction
        start_time = time.time()
        
        # Generate weekly forecast for specific hour
        weekly_forecast = crime_model.predict_weekly_crime_probabilities(
            start_date_str=start_date,
            longitude=longitude,
            latitude=latitude,
            specific_hour=hour
        )
        
        end_time = time.time()
        print(f"Prediction time: {end_time - start_time:.2f} seconds")
        
        # Format the forecast
        formatted_forecast = crime_model.format_weekly_prediction(weekly_forecast)
        
        # Print the formatted forecast
        print("\n" + formatted_forecast)
        
        # Validate the results
        print("\nValidation:")
        
        # Check that we have exactly 7 data points (one for each day of the week)
        if len(weekly_forecast['probabilities']) == 7:
            print(f"✅ Correct number of data points (7 days)")
        else:
            print(f"❌ Unexpected number of data points: {len(weekly_forecast['probabilities'])} (expected 7)")
            
        # Check that all data points are for the specified hour
        all_correct_hour = True
        for dt, _ in weekly_forecast['probabilities']:
            if dt.hour != hour:
                all_correct_hour = False
                print(f"❌ Found data point with incorrect hour: {dt.hour} (expected {hour})")
                break
        
        if all_correct_hour:
            print(f"✅ All data points have the correct hour ({hour})")
            
        # Test cache
        print("\nTesting cache performance...")
        cache_start_time = time.time()
        cached_forecast = crime_model.predict_weekly_crime_probabilities(
            start_date_str=start_date,
            longitude=longitude,
            latitude=latitude,
            specific_hour=hour
        )
        cache_end_time = time.time()
        
        print(f"Cached prediction time: {cache_end_time - cache_start_time:.2f} seconds")
        
        # Verify the cache is working
        if cache_end_time - cache_start_time < (end_time - start_time) / 10:
            print("✅ Cache is working effectively")
        else:
            print("❌ Cache may not be working properly")
            
        print("-" * 50)

def visualize_hourly_pattern():
    """Create a simple ASCII visualization of hourly patterns."""
    print("\n" + "="*80)
    print("Hourly Crime Probability Pattern Visualization")
    print("="*80)
    
    # Find the model path
    model_path = find_model_path()
    
    # Initialize the CrimeModelRAG
    crime_model = CrimeModelRAG(model_path)
    
    # Define downtown Chicago
    latitude = 41.87917
    longitude = -87.62954
    
    # Generate a start date for this week
    today = datetime.now()
    this_week_start = today - timedelta(days=today.weekday())
    start_date = this_week_start.strftime("%Y-%m-%d")
    
    # Generate weekly forecast with 1-hour intervals for detailed pattern
    weekly_forecast = crime_model.predict_weekly_crime_probabilities(
        start_date_str=start_date,
        longitude=longitude,
        latitude=latitude,
        hour_interval=1  # Every hour for detailed pattern
    )
    
    # Get hourly summary
    hourly_summary = weekly_forecast['hourly_summary']
    
    # Print hourly pattern
    print("\nHourly crime probability pattern (average across 7 days):")
    print("Hour  | Probability | Graph")
    print("-" * 50)
    
    # For each hour (0-23)
    for hour in range(24):
        if hour in hourly_summary:
            # Get probability
            prob = hourly_summary[hour]['avg']
            
            # Create bar graph (each * = 5%)
            bar_length = int(prob * 20)
            bar = '*' * bar_length
            
            # Print formatted line
            print(f"{hour:02d}:00 | {prob:.2%}      | {bar}")
    
    print("\nLegend: Each * represents 5% probability")
    print("-" * 50)

if __name__ == "__main__":
    test_handle_default_coordinates()  # Test the new default coordinates handling
    test_weekly_forecast()
    test_weekly_forecast_integration()
    test_specific_hour_forecast()
    visualize_hourly_pattern()
    print("\nAll tests complete!") 