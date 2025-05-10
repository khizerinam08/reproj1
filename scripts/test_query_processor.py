"""
Test script for the query processor component.

This script tests the query processor's ability to extract
time, date, and coordinate information from natural language queries.
"""
import os
import sys
import json
from datetime import datetime, timedelta

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import the query processor
from src.retrieval.query_processor import CrimeQueryProcessor

def test_time_extraction():
    """Test the time extraction functionality."""
    print("\n===== Testing Time Extraction =====")
    processor = CrimeQueryProcessor()
    
    # Test cases for time extraction
    test_cases = [
        # Standard time formats
        ("What's the crime risk at 3pm?", "15:00"),
        ("Is it safe at 10:30 AM?", "10:30"),
        ("Crime probability at 22:45?", "22:45"),
        ("Is it dangerous at midnight?", "00:00"),
        ("Safety at noon in downtown?", "12:00"),
        
        # Time with context words
        ("What's the risk at around 9pm?", "21:00"),
        ("Safety concerns at about 5 in the afternoon?", "17:00"),
        ("Crime data for the area during 8 o'clock in the morning?", "08:00"),
        
        # Time descriptions
        ("Is it safe in the morning?", "09:00"),
        ("Crime risk in the afternoon?", "15:00"),
        ("Safety during the evening hours?", "19:00"),
        ("Risk assessment for night time?", "22:00"),
        
        # Coordinates that should not be treated as times
        ("Crime risk at latitude 41.8781 and longitude -87.6298 at 3pm?", "15:00"),
        ("Safety at coordinates 41.8781, -87.6298 during evening?", "19:00"),
        ("Crime probability at lat 41.8781, lng -87.6298 at 7pm?", "19:00"),
        
        # Tricky cases that previously failed
        ("What's the crime risk at coordinates 41.8781, -87.6298 tonight at 10pm?", "22:00"),
        ("How safe is it to walk around at latitude 41.8781 and longitude -87.6298 tomorrow afternoon?", "15:00"),
        ("What's the crime risk on Friday evening at 41.8781, -87.6298?", "19:00"),
        ("Is it dangerous in South Shore (41.7636, -87.5830) at midnight?", "00:00"),
    ]
    
    for query, expected in test_cases:
        extracted_time = processor.extract_time(query)
        result = "PASS" if extracted_time == expected else "FAIL"
        print(f"{result} - Query: '{query}'")
        print(f"  Expected: '{expected}', Got: '{extracted_time}'")
        
def test_coordinate_extraction():
    """Test the extraction of coordinates from queries."""
    print("\n===== Testing Coordinate Extraction =====")
    
    processor = CrimeQueryProcessor()
    
    test_cases = [
        # Test exact coordinates
        {
            "query": "What's the crime risk at coordinates 41.8781, -87.6298?",
            "expected": (-87.6298, 41.8781, False)
        },
        {
            "query": "Safety at latitude 41.8781 and longitude -87.6298?",
            "expected": (-87.6298, 41.8781, False)
        },
        {
            "query": "Crime stats at lat 41.8781, lng -87.6298?",
            "expected": (-87.6298, 41.8781, False)
        },
        
        # Test with locations
        {
            "query": "How safe is downtown Chicago?", 
            "expected": (-87.6298, 41.8781, False)
        },
        {
            "query": "Crime risk in the Loop?",
            "expected": (-87.6298, 41.8781, False)
        },
        {
            "query": "Safety concerns in Rogers Park?",
            "expected": (-87.6691, 41.9742, False)
        },
        
        # Test with no coordinates (should use default downtown Chicago)
        {
            "query": "What's the crime risk tomorrow at 3pm?",
            "expected": (-87.6298, 41.8781, True)
        },
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        query = test_case["query"]
        expected_lng, expected_lat, expected_default = test_case["expected"]
        
        try:
            longitude, latitude, using_default = processor.extract_coordinates(query)
            
            # Check if coordinates match expected values with some tolerance
            lng_matches = abs(longitude - expected_lng) < 0.0001
            lat_matches = abs(latitude - expected_lat) < 0.0001
            default_matches = using_default == expected_default
            
            if lng_matches and lat_matches and default_matches:
                status = "PASS"
                passed += 1
                print(f"{status} - Query: '{query}'")
                print(f"  Expected: ({expected_lng}, {expected_lat}, {expected_default}), Got: ({longitude}, {latitude}, {using_default})")
            else:
                status = "FAIL"
                failed += 1
                print(f"{status} - Query: '{query}'")
                print(f"  Expected: ({expected_lng}, {expected_lat}, {expected_default}), Got: ({longitude}, {latitude}, {using_default})")
        except Exception as e:
            status = "ERROR"
            failed += 1
            print(f"{status} - Query: '{query}'")
            print(f"  Exception: {e}")
    
    print(f"\nCoordinate Extraction Results: {passed} passed, {failed} failed\n")

def test_date_extraction():
    """Test the date extraction functionality."""
    print("\n===== Testing Date Extraction =====")
    processor = CrimeQueryProcessor()
    
    # Get today's date for relative date testing
    today = datetime.now()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (today + timedelta(days=-1)).strftime("%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")
    
    # Test cases for date extraction
    test_cases = [
        # Relative dates
        ("Crime risk today", today),
        ("Safety tomorrow", tomorrow),
        ("Risk yesterday", yesterday),
        
        # Named days
        ("Crime on Monday", None),  # This depends on the current day
        ("Safety on next Friday", None),  # This depends on the current day
        
        # Specific dates
        ("Crime on January 15th", "2025-01-15"),
        ("Safety on 12/25/2023", "2023-12-25"),
        ("Risk on 2023-10-31", "2023-10-31"),
        
        # Combined with other elements
        ("Crime risk on Friday at 41.8781, -87.6298", None),  # This depends on the current day
        ("Safety on Christmas day at 3pm", "2025-12-25"),
    ]
    
    for query, expected in test_cases:
        extracted_date = processor.extract_date(query)
        # For day-based tests where we can't hardcode the expected result
        if expected is None:
            print(f"INFO - Query: '{query}'")
            print(f"  Got: '{extracted_date}' (dynamic date, manual verification needed)")
            continue
            
        result = "PASS" if extracted_date == expected else "FAIL"
        print(f"{result} - Query: '{query}'")
        print(f"  Expected: '{expected}', Got: '{extracted_date}'")

def test_full_parameter_extraction():
    """Test the full parameter extraction."""
    print("\n===== Testing Full Parameter Extraction =====")
    processor = CrimeQueryProcessor()
    
    test_queries = [
        "What's the crime risk at coordinates 41.8781, -87.6298 tonight at 10pm?",
        "How safe is it to walk around at latitude 41.8781 and longitude -87.6298 tomorrow afternoon?",
        "What's the crime risk on Friday evening at 41.8781, -87.6298?",
        "Is it dangerous in South Shore (41.7636, -87.5830) at midnight?",
        "Should I be worried about safety at 41.9742, -87.6691 on Sunday morning at 8am?",
    ]
    
    for query in test_queries:
        params = processor.extract_parameters(query)
        print(f"\nQuery: '{query}'")
        for key, value in params.items():
            if key != 'original_query':  # Skip printing the full query again
                print(f"  {key}: {value}")

if __name__ == "__main__":
    test_time_extraction()
    test_coordinate_extraction()
    test_date_extraction()
    test_full_parameter_extraction() 