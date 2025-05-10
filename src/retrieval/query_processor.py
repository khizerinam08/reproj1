"""
Query processing for crime prediction queries.

This module contains the CrimeQueryProcessor class which is responsible for
extracting time, date, and coordinate information from natural language queries.
"""
import re
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional, Any, List

class CrimeQueryProcessor:
    """
    Processes natural language queries for crime prediction.
    
    This class extracts time, date, and coordinate information from
    natural language queries to prepare them for the crime prediction model.
    """
    
    def __init__(self):
        """Initialize the query processor."""
        # Load default coordinates (for when only time or date is provided)
        self.default_coordinates = (41.8781, -87.6298)  # Chicago downtown
        
        # Keywords for detecting crime-related queries
        self.crime_keywords = [
            "crime", "safe", "safety", "danger", "dangerous", "risk", 
            "robbery", "theft", "assault", "shooting", "violence", "security"
        ]
        
        # Time periods with default values
        self.time_periods = {
            "morning": "09:00",
            "afternoon": "15:00",
            "evening": "19:00",
            "night": "22:00",
            "dawn": "06:00",
            "dusk": "20:00",
            "midnight": "00:00",
            "noon": "12:00"
        }
        
        # Maintain context from previous queries
        self.context = {
            "longitude": None,
            "latitude": None,
            "date": None,
            "time": None,
            "last_query_type": None
        }
        
    def is_crime_prediction_query(self, query: str) -> bool:
        """
        Determine if a query is asking for crime prediction.
        
        Args:
            query: The natural language query.
            
        Returns:
            True if the query is about crime prediction, False otherwise.
        """
        # Check if query contains coordinate-like patterns
        has_coordinates = bool(re.search(r'\b\d+\.\d+\b', query))
        
        # Check if query contains crime-related keywords
        query_lower = query.lower()
        has_crime_keywords = any(keyword in query_lower for keyword in self.crime_keywords)
        
        # Check if query is asking about a specific time or date
        has_time_reference = bool(re.search(r'\b\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?\b', query) or
                                 any(period in query_lower for period in self.time_periods.keys()))
        
        # Special contextual case: if last query was crime-related and this is a follow-up
        is_followup = self._is_followup_query(query_lower)
        
        # A crime prediction query should have coordinates and be about crime or safety
        return (has_coordinates and has_crime_keywords and has_time_reference) or is_followup
    
    def _is_followup_query(self, query: str) -> bool:
        """
        Determine if a query is a follow-up to a previous crime prediction query.
        
        Args:
            query: The lowercase query string
            
        Returns:
            True if this appears to be a follow-up question
        """
        # If we have no context yet, this can't be a follow-up
        if self.context["last_query_type"] != "crime_prediction":
            return False
            
        # Check for common follow-up patterns
        followup_patterns = [
            r'\bwhat about\b',
            r'\bhow about\b',
            r'\band (on|at|in)\b',
            r'\bwhat if\b',
            r'^(and|but) ',
            r'^(on|at|in) ',
            r'^tomorrow',
            r'^tonight',
            r'^later',
            r'^next',
            r'^is it\b',
            r'^will it be\b',
            r'^(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'^(january|february|march|april|may|june|july|august|september|october|november|december)\b'
        ]
        
        return any(re.search(pattern, query) for pattern in followup_patterns)
    
    def _is_near_coordinate(self, text: str, pos: int) -> bool:
        """Check if the position is near coordinate patterns in the text."""
        # Look for coordinate patterns within 50 characters of the position
        window = 50
        start = max(0, pos - window)
        end = min(len(text), pos + window)
        window_text = text[start:end]
        
        # Check for coordinate patterns
        coord_patterns = [
            r'\b\d+\.\d+\b',  # decimal number
            r'\blatitude\b',
            r'\blongitude\b',
            r'\blat\b',
            r'\blng\b',
            r'\bcoordinates\b'
        ]
        
        # Check if the match itself contains a coordinate pattern
        match_text = text[pos:pos+10]  # Take a small sample from the match position
        if re.search(r'\b\d+\.\d+\b', match_text):
            return True
            
        return any(re.search(pattern, window_text, re.IGNORECASE) for pattern in coord_patterns)
        
    def extract_time(self, query: str) -> str:
        """
        Extract time information from a query.
        
        Args:
            query: The natural language query.
            
        Returns:
            A string representing the time in HH:MM format.
        """
        query_lower = query.lower()
        
        # Check for specific time periods like "midnight" or "noon" first
        if "midnight" in query_lower or "12am" in query_lower or "12 am" in query_lower:
            return "00:00"
        if "noon" in query_lower or "12pm" in query_lower or "12 pm" in query_lower:
            return "12:00"
        
        # Look for specific time formats like "3pm", "10:30 AM", etc.
        time_patterns = [
            # 10:30 AM, 3:45 PM - check this pattern first for minute precision
            (r'\b(\d{1,2}):(\d{2})\s*(am|pm)?\b', 
             lambda m: self._format_hour_minute(m.group(1), m.group(2), m.group(3))),
            
            # 3pm, 10am
            (r'\b(\d{1,2})\s*(pm|am)\b', 
             lambda m: self._format_hour_minute(m.group(1), "00", m.group(2))),
            
            # 22:45, 09:30 (24-hour format)
            (r'\b([01]\d|2[0-3]):([0-5]\d)\b', 
             lambda m: f"{m.group(1)}:{m.group(2)}"),
            
            # o'clock expressions: 8 o'clock
            (r'\b(\d{1,2})\s*o\'clock(?:\s*in the (morning|afternoon|evening))?\b', 
             lambda m: f"{int(m.group(1)) + (12 if m.group(2) == 'afternoon' or m.group(2) == 'evening' else 0):02d}:00"),
            
            # 3 in the afternoon
            (r'\b(\d{1,2})\s*(?:in|during) the (morning|afternoon|evening|night)\b', 
             lambda m: f"{int(m.group(1)) + (12 if m.group(2) == 'afternoon' or m.group(2) == 'evening' else 0):02d}:00")
        ]
        
        # Special patterns for time with "at" preposition in context of coordinates
        coordinate_time_patterns = [
            # at 3pm - typically appears after coordinates
            (r'\bat\s+(\d{1,2})\s*(pm|am)\b', 
             lambda m: self._format_hour_minute(m.group(1), "00", m.group(2))),
            
            # at 10:30 AM - typically appears after coordinates
            (r'\bat\s+(\d{1,2}):(\d{2})\s*(am|pm)?\b', 
             lambda m: self._format_hour_minute(m.group(1), m.group(2), m.group(3)))
        ]
        
        # Check for time patterns that typically appear after coordinates
        for pattern, formatter in coordinate_time_patterns:
            matches = list(re.finditer(pattern, query_lower))
            for match in matches:
                return formatter(match)
        
        # Regular time patterns
        for pattern, formatter in time_patterns:
            matches = list(re.finditer(pattern, query_lower))
            for match in matches:
                # Skip if this is clearly part of a coordinate
                if self._is_near_coordinate(query_lower, match.start()):
                    continue
                return formatter(match)
        
        # Check for specific time periods like "morning", "afternoon", etc.
        for period, default_time in self.time_periods.items():
            if f" {period}" in query_lower:
                # Extra check for "in the afternoon" type phrases
                if f"in the {period}" in query_lower or f"during the {period}" in query_lower:
                    return self.time_periods[period]
                # Check for "about 5 in the afternoon" type phrases
                about_time_match = re.search(fr'\b(?:around|about|at) (\d{{1,2}})\s*(?:in|during) the {period}\b', query_lower)
                if about_time_match:
                    hour = int(about_time_match.group(1))
                    if period == "afternoon":
                        return f"{hour + 12:02d}:00"
                    elif period == "evening":
                        return f"{hour + 12:02d}:00"
                    else:
                        return f"{hour:02d}:00"
                return default_time
                
        # If no time found, use context or default to current time
        if self.context["time"]:
            return self.context["time"]
            
        # Default to current time
        now = datetime.now()
        return f"{now.hour:02d}:{now.minute:02d}"

    def _format_hour_minute(self, hour_str: str, minute_str: str, period: Optional[str] = None) -> str:
        """
        Format hour and minute with AM/PM conversion to 24-hour format.
        
        Args:
            hour_str: Hour as string
            minute_str: Minute as string
            period: Optional period (am/pm)
            
        Returns:
            Formatted time string in HH:MM format
        """
        hour = int(hour_str)
        
        # Handle special case of 12 AM/PM
        if hour == 12:
            if period and period.lower() == 'am':
                hour = 0  # 12 AM = 00:00
            # 12 PM stays as 12
        elif period and period.lower() == 'pm' and hour < 12:
            hour += 12  # Convert to 24-hour format
            
        return f"{hour:02d}:{minute_str}"

    def extract_date(self, query: str) -> str:
        """
        Extract date information from a query.
        
        Args:
            query: The natural language query.
            
        Returns:
            A string representing the date in YYYY-MM-DD format.
        """
        query_lower = query.lower()
        now = datetime.now()
        
        # Check for relative dates like "today", "tomorrow", etc.
        if "today" in query_lower or "tonight" in query_lower:
            return now.strftime("%Y-%m-%d")
        elif "tomorrow" in query_lower:
            tomorrow = now + timedelta(days=1)
            return tomorrow.strftime("%Y-%m-%d")
        elif "yesterday" in query_lower:
            yesterday = now + timedelta(days=-1)
            return yesterday.strftime("%Y-%m-%d")
            
        # Check for day names like "Monday", "Tuesday", etc.
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(days):
            if day in query_lower:
                # Calculate days until the next occurrence of this day
                current_day = now.weekday()
                days_ahead = i - current_day
                if days_ahead <= 0:  # Target day is today or already passed this week
                    days_ahead += 7  # Go to next week
                    
                # If "next" is specified, add another week
                if f"next {day}" in query_lower:
                    days_ahead += 7
                    
                target_date = now + timedelta(days=days_ahead)
                return target_date.strftime("%Y-%m-%d")
                
        # Check for specific dates like "January 15", "12/25/2023", etc.
        date_patterns = [
            # Month day, e.g., "January 15th"
            (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?\b',
             lambda m: f"{now.year}-{['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(m.group(1)) + 1:02d}-{int(m.group(2)):02d}"),
            
            # MM/DD/YYYY
            (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',
             lambda m: f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"),
             
            # YYYY-MM-DD
            (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b',
             lambda m: f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"),
        ]
        
        for pattern, formatter in date_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return formatter(match)
                
        # Check for special dates like "Christmas", "New Year's", etc.
        if "christmas" in query_lower or "christmas day" in query_lower:
            return f"{now.year}-12-25"
        elif "new year" in query_lower or "new year's" in query_lower:
            return f"{now.year}-01-01"
        elif "valentine" in query_lower or "valentine's day" in query_lower:
            return f"{now.year}-02-14"
            
        # Check for context from previous query
        if self.context["date"]:
            return self.context["date"]
                
        # Default to today's date
        return now.strftime("%Y-%m-%d")

    def extract_coordinates(self, query: str) -> Tuple[float, float, bool]:
        """
        Extract coordinate information from a query.
        
        Args:
            query: The natural language query.
            
        Returns:
            A tuple of (longitude, latitude, using_default) where using_default is True
            if default coordinates were used.
        """
        # Patterns for different coordinate formats
        coordinate_patterns = [
            # Format with words: "latitude 41.8781, longitude -87.6298"
            r'latitude\s+(\d+\.\d+)\s*,?\s*longitude\s+(-?\d+\.\d+)',
            r'longitude\s+(-?\d+\.\d+)\s*,?\s*latitude\s+(\d+\.\d+)',
            
            # Abbreviated format: "lat 41.8781, lng -87.6298"
            r'lat\s+(\d+\.\d+)\s*,?\s*lng\s+(-?\d+\.\d+)',
            r'lng\s+(-?\d+\.\d+)\s*,?\s*lat\s+(\d+\.\d+)',
            
            # Negative first: "-87.6298, 41.8781"
            r'(-\d+\.\d+)\s*,\s*(\d+\.\d+)',
            
            # Parentheses format: "(41.8781, -87.6298)"
            r'\((\d+\.\d+)\s*,\s*(-?\d+\.\d+)\)',
            
            # Standard format: "41.8781, -87.6298"
            r'(\d+\.\d+)\s*,\s*(-?\d+\.\d+)',
            
            # Coordinates with space: "41.8781 -87.6298"
            r'(\d+\.\d+)\s+(-?\d+\.\d+)',
        ]
        
        for pattern in coordinate_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                # Extract the coordinates
                if "longitude" in pattern and pattern.find("longitude") < pattern.find("latitude"):
                    # If longitude is mentioned first
                    longitude, latitude = float(match.group(1)), float(match.group(2))
                elif "lng" in pattern and pattern.find("lng") < pattern.find("lat"):
                    # If lng is mentioned first
                    longitude, latitude = float(match.group(1)), float(match.group(2))
                elif pattern == r'(-\d+\.\d+)\s*,\s*(\d+\.\d+)':
                    # Special case for "-87.6298, 41.8781" pattern
                    # For US coordinates where first number is negative and in longitude range
                    if float(match.group(1)) < -30 and float(match.group(2)) > 30:
                        # This is clearly a longitude,latitude pair with swapped order
                        longitude, latitude = float(match.group(1)), float(match.group(2))
                        return longitude, latitude, False
                elif match.group(1).startswith('-') and float(match.group(1)) < -30:
                    # If first value is negative and in longitude range
                    longitude, latitude = float(match.group(1)), float(match.group(2))
                elif match.group(2).startswith('-'):
                    # If second number is negative, assume it's longitude
                    latitude, longitude = float(match.group(1)), float(match.group(2))
                elif "-87" in match.group(2) or "-90" in match.group(2):
                    # If second number contains typical US longitude negative values
                    latitude, longitude = float(match.group(1)), float(match.group(2))
                elif float(match.group(1)) > 0 and float(match.group(1)) < 90 and match.group(1) not in ["-87", "-90"]:
                    # If first number is in latitude range and not a typical longitude
                    latitude, longitude = float(match.group(1)), float(match.group(2))
                    # If longitude is positive in the US, make it negative
                    if longitude > 0 and latitude > 0:
                        longitude = -longitude
                elif float(match.group(1)) < -30:
                    # If first number is likely longitude (very negative)
                    longitude, latitude = float(match.group(1)), float(match.group(2))
                else:
                    # Otherwise, assume standard order: latitude, longitude
                    latitude, longitude = float(match.group(1)), float(match.group(2))
                    
                    # If longitude is positive in the US, make it negative
                    if longitude > 0 and latitude > 0:
                        longitude = -longitude
                
                return longitude, latitude, False
                
        # Check for context from previous query
        if self.context["longitude"] is not None and self.context["latitude"] is not None:
            return self.context["longitude"], self.context["latitude"], False
                
        # Default to Chicago downtown if no coordinates found
        return self.default_coordinates[1], self.default_coordinates[0], True

    def extract_parameters(self, query: str) -> Dict[str, Any]:
        """
        Extract all parameters needed for crime prediction from a query.
        
        Args:
            query: The natural language query.
            
        Returns:
            A dictionary with extracted parameters.
        """
        # Extract time, date, and coordinates
        longitude, latitude, using_default = self.extract_coordinates(query)
        time = self.extract_time(query)
        date = self.extract_date(query)
        
        # Create parameter dictionary
        parameters = {
            "time": time,
            "date": date,
            "longitude": longitude,
            "latitude": latitude,
            "complete": True,  # Indicate if all required parameters were extracted
            "original_query": query,
            "using_default": using_default
        }
        
        # Update context with the current parameters
        self._update_context(parameters)
        
        return parameters

    def _update_context(self, params: Dict[str, Any]) -> None:
        """
        Update the context with the current parameters.
        
        Args:
            params: The parameters extracted from the current query
        """
        # Update context with the current parameters
        self.context["longitude"] = params["longitude"]
        self.context["latitude"] = params["latitude"]
        self.context["date"] = params["date"]
        self.context["time"] = params["time"]
        self.context["last_query_type"] = "crime_prediction"
        
    def reset_context(self) -> None:
        """Reset the context to initial state."""
        self.context = {
            "longitude": None,
            "latitude": None,
            "date": None,
            "time": None,
            "last_query_type": None
        }

    def process_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Process a query to determine if it's a crime prediction query and extract parameters.
        
        Args:
            query: The natural language query.
            
        Returns:
            A dictionary with extracted parameters if it's a crime prediction query,
            None otherwise.
        """
        if self.is_crime_prediction_query(query):
            return self.extract_parameters(query)
        return None 