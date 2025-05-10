# Crime Prediction Chatbot Frontend

This is the frontend application for the Crime Prediction Chatbot. It provides an intuitive interface to access crime prediction data and safety recommendations.

## Getting Started

To run this project locally:

```bash
# Install dependencies
npm install

# Start the development server
npm start
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Features

- **Landing Page**: Introduction to the Crime Prediction Chatbot
- **Chatbot Interface**: Interactive interface to get crime predictions (coming soon)
- **Authentication**: User accounts and profiles (coming soon)

## Project Structure

The project follows a feature-based organization:

```
src/
├── components/         # Reusable components
│   ├── common/         # Shared components
│   ├── Auth/           # Authentication components
│   ├── Chat/           # Chat components
│   └── Map/            # Map components
├── pages/              # Page components
│   ├── Landing/        # Landing page
│   ├── Chatbot/        # Chatbot page
│   └── Auth/           # Authentication pages
├── services/           # API and service integrations
├── context/            # Context providers
├── hooks/              # Custom React hooks
├── utils/              # Helper functions
└── styles/             # Global styles
```

## Technologies Used

- React.js
- React Router
- Tailwind CSS
- Context API for state management

## Color Scheme

The application uses the following color scheme:

- Text: `#ffffff`
- Background: `#000000`
- Primary: `#bc2424`
- Secondary: `#e2e2e2`
- Accent: `#bc2424`

## Next Steps

- Implementation of chatbot functionality
- User authentication and profiles
- Location-based crime data visualization 