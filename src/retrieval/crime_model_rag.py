"""
RAG implementation for crime prediction model.
This module provides interfaces to use the pre-trained crime prediction model
as a knowledge source for the chatbot.
"""
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import os
import math

class CrimeModelRAG:
    """
    Retrieval-Augmented Generation interface for the crime prediction model.
    Provides methods to query the model with natural language and get formatted responses.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the Crime Model RAG with the pre-trained model.
        
        Args:
            model_path: Path to the joblib model file
        """
        try:
            self.model = joblib.load(model_path)
            print(f"Loaded crime prediction model from {model_path}")
            print(f"Model type: {type(self.model)}")
            
            # Cache for weekly predictions to avoid redundant calculations
            self._prediction_cache = {}
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    
    def encode_time_features(self, date_obj: datetime) -> Tuple[float, float, float, float]:
        """
        Encode time features using the same methodology as the training data.
        
        Args:
            date_obj: Datetime object containing date and time information
            
        Returns:
            Tuple of (cos_hour, sin_hour, cos_weekday, sin_weekday)
        """
        # Hour features (0-23 hours) - circular encoding
        hour = date_obj.hour + date_obj.minute/60.0  # Include minutes as fraction of hour
        cos_hour = math.cos(2 * math.pi * hour / 24.0)
        sin_hour = math.sin(2 * math.pi * hour / 24.0)
        
        # Weekday features (0-6, where 0 is Monday) - circular encoding
        weekday = date_obj.weekday()
        cos_weekday = math.cos(2 * math.pi * weekday / 7.0)
        sin_weekday = math.sin(2 * math.pi * weekday / 7.0)
        
        return cos_hour, sin_hour, cos_weekday, sin_weekday
        
    def preprocess_query(self, date_str: str, time_str: str, 
                        longitude: float, latitude: float) -> pd.DataFrame:
        """
        Convert query parameters to model input features.
        
        Args:
            date_str: Date string (YYYY-MM-DD)
            time_str: Time string (HH:MM)
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            
        Returns:
            DataFrame of features ready for model prediction
        """
        # Parse date and time
        date_format = "%Y-%m-%d"
        time_format = "%H:%M"
        date_obj = datetime.strptime(date_str, date_format)
        time_obj = datetime.strptime(time_str, time_format)
        
        # Combine date and time
        date_time = datetime.combine(date_obj.date(), time_obj.time())
        
        # Encode time features
        cos_hour, sin_hour, cos_weekday, sin_weekday = self.encode_time_features(date_time)
        
        # Create feature DataFrame with named columns in the correct order expected by the model
        # ['Latitude', 'Longitude', 'sin_hour', 'cos_hour', 'sin_weekday', 'cos_weekday']
        features = pd.DataFrame([{
            'Latitude': latitude,
            'Longitude': longitude,
            'sin_hour': sin_hour,
            'cos_hour': cos_hour,
            'sin_weekday': sin_weekday,
            'cos_weekday': cos_weekday
        }])
        
        return features
    
    def batch_preprocess_queries(self, datetimes: List[datetime], 
                                longitude: float, latitude: float) -> pd.DataFrame:
        """
        Convert multiple datetime queries to model input features in batch.
        
        Args:
            datetimes: List of datetime objects for predictions
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            
        Returns:
            DataFrame of features ready for model prediction
        """
        # Create a list to hold all feature dictionaries
        features_list = []
        
        # Process each datetime
        for dt in datetimes:
            # Encode time features
            cos_hour, sin_hour, cos_weekday, sin_weekday = self.encode_time_features(dt)
            
            # Add to features list
            features_list.append({
                'Latitude': latitude,
                'Longitude': longitude,
                'sin_hour': sin_hour,
                'cos_hour': cos_hour,
                'sin_weekday': sin_weekday,
                'cos_weekday': cos_weekday,
                # Store original datetime for reference
                '_datetime': dt
            })
        
        # Create DataFrame
        features_df = pd.DataFrame(features_list)
        
        # Return DataFrame with prediction features
        return features_df
        
    def predict_crime_probability(self, date_str: str, time_str: str,
                                longitude: float, latitude: float) -> float:
        """
        Predict crime probability for given parameters.
        
        Args:
            date_str: Date string (YYYY-MM-DD)
            time_str: Time string (HH:MM)
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            
        Returns:
            Probability of crime (0-1)
        """
        features = self.preprocess_query(date_str, time_str, longitude, latitude)
        
        try:
            # Use predict_proba if available (for classifiers)
            if hasattr(self.model, 'predict_proba'):
                prob = self.model.predict_proba(features)[0][1]  # Assuming binary classification with 1=crime
                return prob
            # Otherwise use predict (for regression models)
            else:
                return self.model.predict(features)[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            raise e
    
    def predict_weekly_crime_probabilities(self, 
                                          start_date_str: str, 
                                          longitude: float, 
                                          latitude: float,
                                          hour_interval: int = 3,
                                          specific_hour: Optional[int] = None,
                                          use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate crime probability predictions for an entire week at regular intervals.
        
        Args:
            start_date_str: Start date string in YYYY-MM-DD format
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            hour_interval: Number of hours between predictions (default 3)
            specific_hour: If provided, only generate predictions for this specific hour (0-23)
            use_cache: Whether to use cached results if available
            
        Returns:
            Dictionary containing:
            - 'probabilities': List of tuples with (datetime, probability)
            - 'summary': Statistical summary of the week
            - 'daily_summary': Statistics by day
            - 'hourly_summary': Statistics by hour
        """
        # Create cache key including specific hour if provided
        cache_key = f"{start_date_str}_{longitude}_{latitude}_{hour_interval}"
        if specific_hour is not None:
            cache_key += f"_hour{specific_hour}"
        
        # Check cache
        if use_cache and cache_key in self._prediction_cache:
            return self._prediction_cache[cache_key]
        
        # Parse start date
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        
        # Generate datetimes for the week
        datetimes = []
        current_date = start_date
        for day in range(7):  # 7 days in a week
            if specific_hour is not None:
                # If specific hour is provided, only add that hour
                time_slot = current_date.replace(hour=specific_hour, minute=0)
                datetimes.append(time_slot)
            else:
                # Otherwise add all hours based on interval
                for hour in range(0, 24, hour_interval):
                    # Create datetime for this time slot
                    time_slot = current_date.replace(hour=hour, minute=0)
                    datetimes.append(time_slot)
            # Move to next day
            current_date += timedelta(days=1)
        
        # Prepare batch features
        features_df = self.batch_preprocess_queries(datetimes, longitude, latitude)
        
        # Get prediction features only (exclude datetime)
        prediction_features = features_df.drop('_datetime', axis=1)
        
        # Make predictions
        try:
            if hasattr(self.model, 'predict_proba'):
                # For classifiers
                probabilities = self.model.predict_proba(prediction_features)[:, 1]
            else:
                # For regression models
                probabilities = self.model.predict(prediction_features)
                
            # Combine results with datetimes
            results = []
            for i, dt in enumerate(features_df['_datetime']):
                results.append((dt, float(probabilities[i])))
            
            # Create summary statistics
            summary = {
                'avg_probability': float(np.mean(probabilities)),
                'min_probability': float(np.min(probabilities)),
                'max_probability': float(np.max(probabilities)),
                'std_probability': float(np.std(probabilities))
            }
            
            # Create daily summaries
            daily_summary = {}
            for dt, prob in results:
                day_name = dt.strftime("%A")
                if day_name not in daily_summary:
                    daily_summary[day_name] = []
                daily_summary[day_name].append(prob)
            
            # Calculate statistics for each day
            for day, probs in daily_summary.items():
                daily_summary[day] = {
                    'avg': float(np.mean(probs)),
                    'min': float(np.min(probs)),
                    'max': float(np.max(probs)),
                    'samples': len(probs)
                }
            
            # Create hourly summaries
            hourly_summary = {}
            for dt, prob in results:
                hour = dt.hour
                if hour not in hourly_summary:
                    hourly_summary[hour] = []
                hourly_summary[hour].append(prob)
            
            # Calculate statistics for each hour
            for hour, probs in hourly_summary.items():
                hourly_summary[hour] = {
                    'avg': float(np.mean(probs)),
                    'min': float(np.min(probs)),
                    'max': float(np.max(probs)),
                    'samples': len(probs)
                }
            
            # Create the final result
            final_result = {
                'probabilities': results,
                'summary': summary,
                'daily_summary': daily_summary,
                'hourly_summary': hourly_summary,
                'metadata': {
                    'start_date': start_date_str,
                    'longitude': longitude,
                    'latitude': latitude,
                    'hour_interval': hour_interval,
                    'specific_hour': specific_hour,
                    'total_samples': len(results)
                }
            }
            
            # Cache the result
            self._prediction_cache[cache_key] = final_result
            
            return final_result
            
        except Exception as e:
            print(f"Batch prediction error: {e}")
            raise e
    
    def format_weekly_prediction(self, weekly_prediction: Dict[str, Any]) -> str:
        """
        Format weekly prediction results into a readable text format.
        
        Args:
            weekly_prediction: The result from predict_weekly_crime_probabilities
            
        Returns:
            Formatted string describing weekly predictions
        """
        metadata = weekly_prediction['metadata']
        summary = weekly_prediction['summary']
        daily = weekly_prediction['daily_summary']
        specific_hour = metadata.get('specific_hour')
        
        # Format location and date range
        start_date = datetime.strptime(metadata['start_date'], "%Y-%m-%d")
        end_date = start_date + timedelta(days=6)
        
        result = [
            f"Weekly Crime Probability Forecast",
            f"Location: ({metadata['latitude']:.4f}, {metadata['longitude']:.4f})",
            f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        ]
        
        # Add specific hour information if provided
        if specific_hour is not None:
            # Format the hour in 12-hour format with AM/PM
            hour_12 = specific_hour % 12
            if hour_12 == 0:
                hour_12 = 12
            am_pm = "AM" if specific_hour < 12 else "PM"
            result.append(f"Time: {hour_12}:00 {am_pm} each day")
            result.append(f"Samples: 7 days at the same hour ({metadata['total_samples']} total predictions)")
        else:
            result.append(f"Samples: Every {metadata['hour_interval']} hours, {metadata['total_samples']} total predictions")
        
        result.extend([
            "",
            f"Overall Summary:",
            f"- Average probability: {summary['avg_probability']:.1%}",
            f"- Range: {summary['min_probability']:.1%} to {summary['max_probability']:.1%}",
            "",
            f"Daily Breakdown:"
        ])
        
        # Add daily summaries (sorted by day of week, starting with Monday)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in day_order:
            if day in daily:
                stats = daily[day]
                # If specific hour, we only have one data point per day
                if specific_hour is not None:
                    result.append(f"- {day}: {stats['avg']:.1%} crime probability")
                else:
                    result.append(f"- {day}: {stats['avg']:.1%} avg ({stats['min']:.1%} to {stats['max']:.1%})")
        
        result.append("")
        result.append("Risk Assessment:")
        
        # Find safest and riskiest days
        safest_day = min(daily.items(), key=lambda x: x[1]['avg'])[0]
        riskiest_day = max(daily.items(), key=lambda x: x[1]['avg'])[0]
        
        result.append(f"- Safest day: {safest_day}")
        result.append(f"- Highest risk day: {riskiest_day}")
        
        # Add hourly information only if we have multiple hours
        hourly = weekly_prediction['hourly_summary']
        if hourly and specific_hour is None:
            safest_hour = min(hourly.items(), key=lambda x: x[1]['avg'])[0]
            riskiest_hour = max(hourly.items(), key=lambda x: x[1]['avg'])[0]
            
            # Convert to 12-hour format
            safest_hour_12 = safest_hour % 12
            if safest_hour_12 == 0:
                safest_hour_12 = 12
            safest_am_pm = "AM" if safest_hour < 12 else "PM"
            
            riskiest_hour_12 = riskiest_hour % 12
            if riskiest_hour_12 == 0:
                riskiest_hour_12 = 12
            riskiest_am_pm = "AM" if riskiest_hour < 12 else "PM"
            
            result.append(f"- Safest time: {safest_hour_12}:00 {safest_am_pm}")
            result.append(f"- Highest risk time: {riskiest_hour_12}:00 {riskiest_am_pm}")
        
        # Return the formatted result
        return "\n".join(result)
        
    def generate_explanation(self, probability: float, 
                           query_params: Dict) -> str:
        """
        Generate a natural language explanation of the prediction.
        
        Args:
            probability: The predicted probability
            query_params: The parameters used for prediction
            
        Returns:
            A formatted explanation string
        """
        # Format the date and time for display
        date_str = query_params['date']
        time_str = query_params['time']
        lat = query_params['latitude']
        lng = query_params['longitude']
        
        # Check for default parameters
        using_default = query_params.get('using_default', {})
        if isinstance(using_default, bool):  # For backward compatibility
            using_default = {'coordinates': using_default}
            
        # Check if we're missing any essential parameters
        if using_default.get('coordinates', False):
            return (
                "I notice you didn't specify a location in your query. "
                "To provide accurate crime risk predictions, I need a specific location. "
                "Please specify a location by providing coordinates or a place name. "
                "For example: 'What's the crime risk at 41.8781, -87.6298 tonight?' or "
                "'Is it safe in downtown Chicago at 10pm?'"
            )
        elif using_default.get('time', False) and using_default.get('date', False):
            return (
                "I notice you didn't specify a time or date in your query. "
                "To provide accurate crime risk predictions, I need a specific time and date. "
                "Please specify when you'd like a prediction for. "
                "For example: 'What's the crime risk in downtown Chicago tonight at 10pm?' or "
                "'Is it safe at 41.8781, -87.6298 tomorrow morning?'"
            )
        elif using_default.get('time', False):
            return (
                "I notice you didn't specify a time in your query. "
                "To provide accurate crime risk predictions, I need a specific time. "
                "Please specify what time you'd like a prediction for. "
                "For example: 'What's the crime risk in downtown Chicago at 10pm?' or "
                "'Is it safe at 41.8781, -87.6298 at 7am?'"
            )
        elif using_default.get('date', False):
            return (
                "I notice you didn't specify a date in your query. "
                "To provide accurate crime risk predictions, I need a specific date. "
                "Please specify what date you'd like a prediction for. "
                "For example: 'What's the crime risk in downtown Chicago tomorrow?' or "
                "'Is it safe at 41.8781, -87.6298 on Friday?'"
            )
        
        # Convert probability to percentage
        prob_percent = probability * 100
        
        # Risk level categorization
        if prob_percent < 20:
            risk_level = "very low"
        elif prob_percent < 40:
            risk_level = "low"
        elif prob_percent < 60:
            risk_level = "moderate"
        elif prob_percent < 80:
            risk_level = "high"
        else:
            risk_level = "very high"
            
        # Generate explanation
        explanation = (
            f"For the location at coordinates ({lat:.4f}, {lng:.4f}) "
            f"on {date_str} at {time_str}, "
            f"the model predicts a {risk_level} risk of crime "
            f"with a probability of {prob_percent:.1f}%."
        )
        
        # Add time-based factors
        date_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        weekday_name = date_obj.strftime("%A")
        hour = date_obj.hour
        
        if hour >= 0 and hour < 6:
            time_context = "late night/early morning"
        elif hour >= 6 and hour < 12:
            time_context = "morning"
        elif hour >= 12 and hour < 18:
            time_context = "afternoon"
        else:
            time_context = "evening"
            
        explanation += f" The prediction takes into account that this is a {weekday_name} {time_context}."
        
        return explanation 