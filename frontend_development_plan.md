# Frontend Development Plan for Crime Prediction Chatbot

This document outlines the simplified frontend development strategy for the Crime Prediction Chatbot, organized into 5 key milestones.

## Overview

We will create a modern, responsive web interface for the Crime Prediction Chatbot that allows users to:
- Ask questions about crime risks in natural language
- View crime predictions for specific locations and times
- Generate and visualize weekly crime forecasts
- Sign in and create accounts to save preferences
- Interact with maps to select locations

## Technology Stack

- **Framework**: React.js with JavaScript
- **State Management**: Context API
- **UI Components**: Material-UI or Chakra UI
- **Maps Integration**: Mapbox or Google Maps API
- **API Communication**: Axios or Fetch API
- **Styling**: Tailwind CSS

## Folder Structure

```
frontend/
├── public/             # Static files
│   ├── index.html
│   └── assets/         # Images, icons, etc.
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── Chat/       # Chat components
│   │   ├── Auth/       # Authentication components
│   │   ├── Map/        # Map components
│   │   └── common/     # Buttons, inputs, etc.
│   ├── pages/          # Page components
│   │   ├── Landing/    # Landing page
│   │   ├── Chatbot/    # Main chatbot interface
│   │   └── Auth/       # Sign in/login pages
│   ├── services/       # API and service integrations
│   │   ├── api.js      # API client
│   │   ├── mapService.js
│   │   └── authService.js
│   ├── hooks/          # Custom React hooks
│   ├── context/        # Context providers
│   ├── utils/          # Helper functions
│   ├── styles/         # Global styles
│   ├── App.js          # Main application component
│   └── index.js        # Entry point
├── package.json
└── tailwind.config.js
```

## Milestone 1: Project Setup and Landing Page

**Goal**: Set up the project structure and implement the landing page.

**Tasks**:
1. Initialize React project with JavaScript
2. Set up routing with React Router
3. Create basic layout components (Header, Footer)
4. Implement landing page with:
   - Hero section explaining the service
   - Features highlights
   - Call to action to sign up or use the chatbot
5. Set up styling system with Tailwind CSS
6. Implement responsive design foundations

**Deliverable**: A static, functional landing page with navigation to other pages.

## Milestone 2: Authentication System

**Goal**: Implement user sign-up and login functionality.

**Tasks**:
1. Create sign-up form component
2. Implement login form component
3. Build form validation
4. Create authentication service
5. Implement protected routes
6. Build user context provider
7. Add persistent login with MongoDB
8. Create account recovery flow (forgot password)

**Deliverable**: Functional authentication system that allows users to create accounts and log in.

## Milestone 3: Chatbot Interface

**Goal**: Implement the main chatbot interface for crime prediction queries.

**Tasks**:
1. Create chat container component
2. Implement message components (user and bot)
3. Build chat input with send functionality
4. Create chat history display
5. Implement API service to communicate with backend
6. Add message loading states
7. Implement error handling for failed requests
8. Create special command handling (e.g., /weekly)

**Deliverable**: A functional chatbot interface that can send and receive messages.

## Milestone 4: Map Integration

**Goal**: Implement map functionality for location selection in the chatbot.

**Tasks**:
1. Integrate map library (Mapbox or Google Maps)
2. Create location selection component
3. Implement geocoding for address to coordinates conversion
4. Build coordinate display within chat messages
5. Implement current location detection
6. Add location markers and info windows
7. Integrate map with chatbot queries

**Deliverable**: A functional map interface integrated with the chatbot for location selection.

## Milestone 5: Enhanced UI and User Experience

**Goal**: Polish the UI and implement advanced UX features.

**Tasks**:
1. Implement theme switching (light/dark mode)
2. Add animations and transitions for smoother UX
3. Create saved locations functionality for logged in users
4. Implement notification system for high-risk alerts
5. Build user preferences storage
6. Add keyboard shortcuts
7. Implement accessibility features
8. Create mobile-optimized views
9. Final performance optimization

**Deliverable**: A polished, production-ready frontend application.

## Design Inspiration

Look to these sources for UI/UX inspiration:

1. **Landing Pages**:
   - Stripe.com - Clean, modern design with clear value proposition
   - Slack.com - Simple but engaging landing page
   - Notion.so - Minimalist design with clear call to action

2. **Authentication**:
   - Google sign-in page - Simple, clean authentication
   - Airbnb login flow - User-friendly registration
   - Dropbox authentication - Clear error handling and guidance

3. **Chat Interfaces**:
   - OpenAI's ChatGPT interface
   - Google Maps' location chat functionality
   - Intercom's chat widget

4. **Maps and Location**:
   - Uber's location selection UI
   - Airbnb's map interface
   - Google Maps' place details

## Implementation Resources

- **Component Libraries**:
  - [Material UI](https://mui.com/)
  - [Chakra UI](https://chakra-ui.com/)

- **Map Libraries**:
  - [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
  - [Google Maps API](https://developers.google.com/maps/documentation/javascript/overview)
  - [React Leaflet](https://react-leaflet.js.org/)

- **Authentication**:
  - [Firebase Authentication](https://firebase.google.com/docs/auth)
  - [Auth0](https://auth0.com/)
  - [JWT Authentication](https://jwt.io/)

- **UI Inspiration**:
  - [Dribbble](https://dribbble.com/) - Search for "chat interface" or "login page"
  - [Behance](https://www.behance.net/)
  - [UI8](https://ui8.net/) - For premium UI kits

## Integration with Backend

The frontend will communicate with the existing Python backend through a RESTful API. Key endpoints will include:

1. `/api/auth` - For authentication requests
2. `/api/chat` - For sending messages and receiving responses
3. `/api/location/validate` - For validating location coordinates

Ensure proper CORS configuration on the backend to allow frontend requests. 