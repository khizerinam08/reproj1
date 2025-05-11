# Crime Prediction Chatbot Backend

This is the backend for the Crime Prediction Chatbot application, providing authentication and chat storage services.

## Features

- User authentication (register, login, profile)
- MongoDB integration for data storage
- JWT-based authentication
- Chat functionality with user-specific chats
- Password encryption with bcrypt

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- MongoDB (local or Atlas)

### Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/crime_prediction
   JWT_SECRET=your_jwt_secret_key_change_in_production
   JWT_EXPIRE=24h
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. For production:
   ```
   npm start
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/profile` - Get user profile (protected)

### Chats

- `GET /api/chats` - Get all user chats (protected)
- `POST /api/chats` - Create a new chat (protected)
- `GET /api/chats/:id` - Get a specific chat (protected)
- `DELETE /api/chats/:id` - Delete a chat (protected)
- `POST /api/chats/:id/messages` - Add a message to a chat (protected)

## Testing

Run the test script to verify the authentication and chat functionality:

```
npm install axios --save-dev
node test.js
```

Make sure the server is running before executing the tests.

## Folder Structure

```
backend/
  ├── config/          # Configuration files
  │   └── db.js        # MongoDB connection
  ├── controllers/     # Route controllers
  │   ├── authController.js
  │   └── chatController.js
  ├── middleware/      # Middleware functions
  │   └── auth.js      # Authentication middleware
  ├── models/          # Mongoose models
  │   ├── User.js
  │   └── Chat.js
  ├── routes/          # API routes
  │   ├── auth.js
  │   └── chat.js
  ├── .env             # Environment variables
  ├── server.js        # Main server file
  ├── test.js          # Test script
  └── package.json
``` 