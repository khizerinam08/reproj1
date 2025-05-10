"""
Command handling for the CLI interface.
"""
from typing import Dict, Any, List, Tuple, Optional
import re
from datetime import datetime

from src.llm.ollama_client import OllamaClient
from src.retrieval.crime_model_rag import CrimeModelRAG
from src.retrieval.query_processor import CrimeQueryProcessor
from src.retrieval.rag_manager import RAGManager
from src.memory.conversation import ConversationMemory


class CommandHandler:
    """Handles commands entered by users."""

    def __init__(
        self,
        llm_client: OllamaClient,
        crime_model: CrimeModelRAG,
        memory: ConversationMemory,
        query_processor: CrimeQueryProcessor,
        rag_manager: RAGManager,
    ):
        self.llm_client = llm_client
        self.crime_model = crime_model
        self.memory = memory
        self.query_processor = query_processor
        self.rag_manager = rag_manager
        self.commands = {
            '/help': self.show_help,
            '/clear': self.clear_memory,
            '/history': self.show_history,
            '/weekly': self.weekly_forecast,
        }

    def process_command(self, command: str) -> str:
        """Process a command and return the response."""
        command = command.strip()
        
        # Extract command name and arguments
        parts = command.split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd_name in self.commands:
            return self.commands[cmd_name](args)
        else:
            return f"Unknown command: {cmd_name}. Type /help for available commands."

    def show_help(self, _: str) -> str:
        """Show available commands."""
        help_text = """
Available commands:
/help - Show this help message
/clear - Clear conversation history
/history - Show conversation history
/weekly [location] [at HOUR] - Get weekly crime forecast for a location

Examples:
/weekly downtown chicago
/weekly 41.8781,-87.6298
/weekly downtown chicago at 10pm
/weekly 41.8781,-87.6298 at 8am
"""
        return help_text

    def clear_memory(self, _: str) -> str:
        """Clear conversation memory."""
        self.memory.clear()
        return "Conversation history cleared."

    def show_history(self, _: str) -> str:
        """Show conversation history."""
        history = self.memory.get_history()
        if not history:
            return "No conversation history."
        
        formatted_history = ""
        for entry in history:
            role = "You" if entry["role"] == "user" else "Bot"
            formatted_history += f"{role}: {entry['content']}\n\n"
        
        return formatted_history
    
    def weekly_forecast(self, args: str) -> str:
        """Generate a weekly crime forecast for a location."""
        if not args:
            return "Please provide a location. Example: /weekly downtown chicago"
        
        if not self.crime_model:
            return "Weekly forecasting is unavailable. Crime prediction model not loaded."
        
        # Default values
        specific_hour = None
        location_args = args
        
        # Check if specific hour is provided
        hour_pattern = r'(?:at|@)\s*(\d{1,2})(?:\s*(?:am|pm|[AaPp][Mm]))?(?:\s*hours?)?'
        hour_match = re.search(hour_pattern, args)
        
        if hour_match:
            # Extract the hour
            hour_str = hour_match.group(1)
            hour_value = int(hour_str)
            
            # Check if AM/PM specified
            am_pm = re.search(r'([AaPp][Mm])', args)
            if am_pm:
                if am_pm.group(1).lower() == 'pm' and hour_value < 12:
                    hour_value += 12
                elif am_pm.group(1).lower() == 'am' and hour_value == 12:
                    hour_value = 0
            
            # Validate hour
            if 0 <= hour_value <= 23:
                specific_hour = hour_value
                # Remove hour specification from location args
                location_args = args.replace(hour_match.group(0), '').strip()
            else:
                return f"Invalid hour specified: {hour_value}. Hour must be between 0-23."
        
        # Check if we have coordinates directly
        coord_pattern = r'(-?\d+\.?\d*),\s*(-?\d+\.?\d*)'
        coord_match = re.search(coord_pattern, location_args)
        
        if coord_match:
            # Direct coordinates provided
            latitude = float(coord_match.group(1))
            longitude = float(coord_match.group(2))
            location_name = location_args
            using_default = False
        else:
            # Try to extract coordinates using query processor
            try:
                # Try to extract coordinates from the query
                coordinates_result = self.query_processor.extract_coordinates(location_args)
                
                if len(coordinates_result) == 3:  # New format with using_default flag
                    longitude, latitude, using_default_coords = coordinates_result
                else:  # Legacy format for backward compatibility
                    longitude, latitude = coordinates_result
                    using_default_coords = False
                
                location_name = location_args
                
                # Check if we're using default coordinates
                if using_default_coords:
                    return (
                        "I need a specific location to generate a weekly crime forecast. "
                        "Please provide a location by specifying coordinates or a place name. "
                        "For example: /weekly 41.8781,-87.6298 or /weekly downtown chicago"
                    )
            except Exception as e:
                return f"Error processing location: {str(e)}"
        
        # Get the current date as start date
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Generate weekly forecast
            weekly_forecast = self.crime_model.predict_weekly_crime_probabilities(
                start_date_str=start_date,
                longitude=longitude,
                latitude=latitude,
                hour_interval=6,  # Every 6 hours
                specific_hour=specific_hour  # Optional specific hour
            )
            
            # Format the forecast
            formatted_forecast = self.crime_model.format_weekly_prediction(weekly_forecast)
            
            # Add location name and hour to the output
            response = f"Weekly Crime Forecast for {location_name}"
            if specific_hour is not None:
                # Format hour in 12-hour format with AM/PM
                hour_12 = specific_hour % 12
                if hour_12 == 0:
                    hour_12 = 12
                am_pm = "AM" if specific_hour < 12 else "PM"
                response += f" at {hour_12}{am_pm}"
            
            response += "\n\n" + formatted_forecast
            
            return response
        except Exception as e:
            return f"Error generating weekly forecast: {str(e)}" 