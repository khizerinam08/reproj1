# Crime Prediction Chatbot with Weekly Forecasting

A context-aware crime prediction chatbot that provides crime risk assessments for specific locations and times, now with weekly forecasting capabilities.

## Features

- **Point Predictions**: Get crime risk assessment for a specific location, date, and time
- **Context-Aware Follow-up Questions**: Ask follow-up questions without repeating the context
- **Weekly Crime Forecasting**: Generate crime probability forecasts for an entire week
- **Hour-Specific Weekly Forecasts**: View crime patterns for a specific hour across all days of the week
- **Interactive CLI Interface**: User-friendly command-line interface with colorful output
- **Batch Prediction Engine**: Efficiently generate predictions for multiple time points
- **Location Verification**: Requires explicit location information for accurate predictions

## Weekly Forecasting Feature

The weekly forecasting feature allows users to:

- View crime probabilities over an entire week for a specific location
- Filter forecasts to a specific hour of the day (e.g., every day at 10 PM)
- Identify high-risk and low-risk days and times
- Understand crime risk patterns throughout the day and week
- Make more informed decisions about safety planning

### Commands

```
/weekly [location] [at HOUR] - Generate a weekly crime forecast for a location
```

Examples:
```
/weekly downtown chicago
/weekly 41.8781,-87.6298
/weekly downtown chicago at 10pm
/weekly 41.8781,-87.6298 at 8am
```

### Example Output

**Full weekly forecast:**
```
Weekly Crime Forecast for downtown chicago

Weekly Crime Probability Forecast
Location: (41.8792, -87.6295)
Period: 2023-05-01 to 2023-05-07
Samples: Every 6 hours, 28 total predictions

Overall Summary:
- Average probability: 25.0%
- Range: 0.0% to 100.0%

Daily Breakdown:
- Monday: 25.0% avg (0.0% to 100.0%)
- Tuesday: 25.0% avg (0.0% to 100.0%)
- Wednesday: 25.0% avg (0.0% to 100.0%)
- Thursday: 25.0% avg (0.0% to 100.0%)
- Friday: 25.0% avg (0.0% to 100.0%)
- Saturday: 25.0% avg (0.0% to 100.0%)
- Sunday: 25.0% avg (0.0% to 100.0%)

Risk Assessment:
- Safest day: Monday
- Highest risk day: Monday
- Safest time: 6:00 AM
- Highest risk time: 12:00 AM
```

**Hour-specific forecast:**
```
Weekly Crime Forecast for downtown chicago at 10PM

Weekly Crime Probability Forecast
Location: (41.8792, -87.6295)
Period: 2023-05-01 to 2023-05-07
Time: 10:00 PM each day
Samples: 7 days at the same hour (7 total predictions)

Overall Summary:
- Average probability: 0.0%
- Range: 0.0% to 0.0%

Daily Breakdown:
- Monday: 0.0% crime probability
- Tuesday: 0.0% crime probability
- Wednesday: 0.0% crime probability
- Thursday: 0.0% crime probability
- Friday: 0.0% crime probability
- Saturday: 0.0% crime probability
- Sunday: 0.0% crime probability

Risk Assessment:
- Safest day: Monday
- Highest risk day: Monday
```

## Location Handling

The system now includes improved location handling:

- **Required Location Information**: All crime predictions require explicit location information
- **No Default Assumptions**: The system will not make predictions using assumed locations
- **Clear User Guidance**: When location is missing, the system provides helpful instructions
- **Context Preservation**: For follow-up questions, the system remembers previously mentioned locations

When a user asks a question without providing location information, instead of using default coordinates, the system will prompt the user to provide a specific location:

```
User: What's the crime risk tonight at 10pm?

System: I notice you didn't specify a location in your query. 
To provide accurate crime risk predictions, I need a specific location. 
Please specify a location by providing coordinates or a place name. 
For example: 'What's the crime risk at 41.8781, -87.6298 tonight?' or 
'Is it safe in downtown Chicago at 10pm?'
```

## Technical Implementation

The weekly forecasting feature is implemented through:

1. **Batch Prediction Engine**: Efficiently generates predictions for every hour across a 7-day period
2. **Hour Filtering**: Allows filtering predictions to a specific hour across all days
3. **Time Encoding**: Properly encodes time features for model input
4. **Caching System**: Stores predictions to avoid redundant calculations
5. **Statistical Summaries**: Calculates meaningful statistics (min, max, avg) for days and hours
6. **Formatted Reports**: Generates human-readable reports from the prediction data
7. **Location Verification**: Detects and flags when default coordinates would be used

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place your crime prediction model at one of these locations:
   - `crime_model.pkl`
   - `models/crime_model.pkl`
   - `data/models/crime_model.pkl`
4. Run the chatbot: `python src/interface/cli.py`

## Running Tests

To test the weekly forecasting feature:

```
python scripts/test_weekly_forecasting.py
```

This will test default location handling and generate sample forecasts for different locations and visualize hourly patterns.

## Future Enhancements

- Web interface with interactive heatmaps for weekly forecasts
- Customizable reports with user preferences
- Exportable PDF reports for safety planning
- Comparative analysis between different locations
- Location name resolution using geocoding services

## Overview

This project implements an AI-powered conversational interface for crime prediction analysis. The system combines several key components:

1. **LLM Integration**: Connects to Ollama for natural language processing
2. **Crime Prediction Model**: Uses a trained model to predict crime probability
3. **Retrieval-Augmented Generation (RAG)**: Enhances responses with relevant information
4. **Contextual Query Processing**: Maintains conversation context for follow-up questions

The primary goal is to provide users with accurate crime risk assessments while maintaining a conversational flow that feels natural.

## Key Features

### Context-Aware Follow-up Question Handling

The chatbot can handle follow-up questions that reference previous queries. For example:

```
User: What's the crime risk at coordinates 41.8781, -87.6298 on Thursday at 10pm?
Bot: [Provides assessment]

User: What about Friday? 
Bot: [Understands this refers to the same location but a different day]

User: Is it safer during the day?
Bot: [Recognizes this refers to the same location and updates only the time]
```

### Adaptive Parameter Extraction

The system intelligently extracts and maintains parameters across a conversation:

- **Location Tracking**: Remembers coordinates from previous queries
- **Time Context**: Carries over time references when only partial information is provided
- **Date Understanding**: Processes relative date references ("tomorrow", "next Monday")

### Natural Conversation Flow

- Handles vague or incomplete queries by using context
- Responds to different types of follow-up patterns
- Maintains a concise, focused communication style

## Technical Components

### Query Processing

- `CrimeQueryProcessor`: Extracts parameters from natural language, maintains conversational context
- Pattern matching: Uses regex to extract coordinates, time, and date information
- Context management: Stores and updates parameters between queries

### Retrieval System

- `RAGManager`: Integrates with the crime prediction model to provide risk assessments
- `OllamaClient`: Manages communication with the LLM for natural language generation
- Context-aware prompting: Augments prompts with information about conversation history

### CLI Interface

- Interactive terminal interface for communicating with the crime prediction bot
- Command handling for saving/loading conversations and clearing history
- Colorized output for better readability

## Usage Examples

### Basic Crime Risk Query

```
User: What's the crime risk at 41.8781, -87.6298 tonight at 10pm?
Bot: Based on our crime prediction model, the probability of crime at those coordinates 
     tonight at 10pm is extremely low, with a predicted risk of 0.0%.
```

### Follow-up Queries

```
User: Is it safe at latitude 41.8781 and longitude -87.6298 tonight?
Bot: [Risk assessment for tonight]

User: What about at 41.7636, -87.5830?
Bot: [Risk assessment for the new location, same time]

User: And downtown?
Bot: [Risk assessment for downtown, same time]
```

### Multiple Parameter Changes

```
User: Crime risk at 41.8781, -87.6298 on Monday at 3pm?
Bot: [Risk assessment]

User: What about Wednesday night?
Bot: [Updated assessment for Wednesday night, same location]
```

## Implementation Details

The system uses a combination of:

1. Context tracking in the `CrimeQueryProcessor` class
2. Follow-up detection patterns to identify questions that reference previous queries
3. Parameter extraction with fallback to previous context when information is missing
4. Enhanced prompting to guide the LLM in using conversation history appropriately

## Future Improvements

- Expanded follow-up pattern recognition
- Better handling of relative time expressions ("an hour later", "next morning")
- Improved location recognition for named places without coordinates
- Integration with user preferences for personalized safety assessments

## Features

- **Streaming Responses**: Real-time, token-by-token response generation for a fluid chat experience
- **Crime Prediction Focus**: Specialized for crime risk assessment with broader conversational capabilities
- **RAG Integration**: Retrieval-Augmented Generation using a crime prediction model
- **Conversation Memory**: Maintains context throughout the conversation
- **CLI Interface**: Simple command-line interface with colorized output

## How It Works

1. **Crime Risk Model**: Uses a machine learning model trained on historical crime data to estimate risk levels based on:
   - Location (latitude/longitude coordinates)
   - Time of day
   - Day of week

2. **Natural Language Processing**: Extracts location and time information from natural language queries

3. **Streaming Response Generation**: Sends generated text to the interface in real-time for a smooth user experience

4. **Flexible Conversations**: Maintains focus on crime-related topics while allowing for general discussion and greetings

## Requirements

- Python 3.8+
- Ollama (for local LLM)
- Required Python packages (install via `pip install -r requirements.txt`):
  - langchain
  - joblib
  - scikit-learn
  - pandas
  - numpy
  - pyyaml
  - requests

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Ollama from [ollama.ai](https://ollama.ai) and pull the Llama 3 model:
   ```
   ollama pull llama3:8b
   ```

3. Run the CLI interface:
   ```
   python src/interface/cli.py
   ```

## Sample Queries

### Specific Crime Predictions
```
What's the crime risk at coordinates 41.8781, -87.6298 tonight at 10pm?
```

```
Is it safe to walk around at latitude 40.7128, longitude -74.0060 tomorrow morning?
```

### General Crime Topics
```
What are the current trends in urban crime rates?
```

```
How do crime statistics vary across different countries?
```

```
What factors contribute to higher crime rates in certain areas?
```

### Basic Interaction
```
Hello, can you tell me what you do?
```

```
How can you help me with crime prediction?
```

## How to Use

- The assistant's primary function is crime prediction based on:
  - Location (coordinates)
  - Time/date information
- The system will prompt for any missing information needed to make a prediction
- You can also engage in general conversations about crime trends and statistics
- Basic greetings and questions about the assistant's capabilities are also supported

## Development

- `src/llm/`: Ollama client and LLM interface
- `src/retrieval/`: RAG components and query processor
- `src/memory/`: Conversation history management
- `src/interface/`: CLI interface with streaming support
- `src/utils/`: Helper functions and utilities

## Notes

- This is a specialized demonstration tool using a trained model
- Risk assessments are based on statistical patterns and should not be the sole factor in safety decisions
- The model does not have access to real-time crime data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Crime Prediction Chatbot

A conversational interface for crime prediction based on location, time, and date.

### Features

- **Natural language queries**: Ask questions about crime risk in plain English
- **Contextual prediction**: Get predictions based on location, time, and date
- **Weekly forecasting**: Generate crime forecasts for an entire week
- **Location handling**: Requires explicit location for accurate predictions
- **Real-time responses**: Fast, efficient crime risk assessment
- **Parameter memory**: Context preservation for follow-up questions

### System Requirements

The system now requires a real crime prediction model to function properly. The mock model has been removed from the codebase.

#### Crime Prediction Model

To use this system, you need a trained crime prediction model that meets these requirements:

1. The model must be saved as a joblib file named `crime_model.pkl`
2. The model should accept features in the following order:
   - cos_hour: Cosine transformation of hour (time cyclical feature)
   - sin_hour: Sine transformation of hour (time cyclical feature)
   - cos_weekday: Cosine transformation of weekday (day cyclical feature)
   - sin_weekday: Sine transformation of weekday (day cyclical feature)
   - longitude: Geographic longitude coordinate
   - latitude: Geographic latitude coordinate
3. The model should return probabilities between 0 and 1

#### Model Installation

Place your `crime_model.pkl` file in one of these locations:
- Project root directory
- `models/` directory
- `data/models/` directory

Alternatively, you can specify a custom path in the configuration file.

### Location Handling

All crime predictions require explicit location information:
- The system will not make predictions using assumed locations
- Clear user guidance is provided when location is missing
- Context is preserved for follow-up questions, remembering previously mentioned locations

Example interaction:
```
User: Is my daily 7am commute safe?
AI: To predict crime risk, I need more information about location coordinates. 
    Please provide these details. For example: 'What's the crime risk at 41.8781, -87.6298?' 
    or 'Is it safe in downtown Chicago?'

User: What about downtown Chicago?
AI: For the location at coordinates (41.8781, -87.6298) in downtown Chicago on [date] at 07:00, 
    the model predicts a very low risk of crime with a probability of 0.2%. 
    The prediction takes into account that this is a Monday morning.
```

### Weekly Forecasting

The weekly forecast feature provides crime predictions for each day of the week:

```
/weekly Chicago downtown
```

This will generate a detailed forecast showing crime probabilities for each day, with risk categorization.

### Setup and Installation

1. Clone the repository
2. Install the required packages: `pip install -r requirements.txt`
3. Place your `crime_model.pkl` file in one of the expected locations
4. Run the application: `python -m src.app` 