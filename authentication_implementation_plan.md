# Authentication System Implementation Plan

This document outlines a detailed implementation plan for the Authentication System (Milestone 2) of our Crime Prediction Chatbot frontend. The plan is divided into 6 sequential sub-milestones for easier implementation and tracking, now including MongoDB backend setup.

## Overview

The authentication system will allow users to:
- Create new accounts (stored in MongoDB)
- Log in to existing accounts
- Reset forgotten passwords
- Maintain persistent sessions
- Access protected routes/features
- Store and retrieve user-specific chat history

## Dependencies

### Frontend Dependencies
```bash
npm install axios react-hook-form yup
```

These will help with:
- API communication (axios)
- Form validation (react-hook-form, yup)

### Backend Dependencies
```bash
npm install express mongoose bcrypt jsonwebtoken cors dotenv
```

These will help with:
- Server creation (express)
- MongoDB connection and modeling (mongoose)
- Password hashing (bcrypt)
- Token generation (jsonwebtoken)
- Cross-origin requests (cors)
- Environment variable management (dotenv)

## Milestone 2.1: MongoDB Backend Setup

**Goal**: Create a backend server with MongoDB integration for user authentication and chat storage.

**Tasks**:

1. **Setup Express Server**:
   - Create a new directory for the backend
   - Initialize npm and install dependencies
   - Create the basic Express server structure
   - Set up CORS to allow frontend requests

2. **Configure MongoDB Connection**:
   - Set up environment variables for MongoDB connection
   - Create connection logic with Mongoose
   - Add connection error handling and logging

3. **Create Data Models**:
   - Create User model with fields for email, password, name, etc.
   - Create Chat model with user reference and message history
   - Implement password hashing with bcrypt

4. **Implement Authentication Routes**:
   - Create registration endpoint
   - Create login endpoint that returns JWT
   - Implement password reset endpoints
   - Create endpoint for validating tokens

5. **Implement Chat Routes**:
   - Create endpoints for fetching user-specific chats
   - Add routes for creating and updating chats
   - Implement middleware to verify user authentication

**Files to Create**:
```
backend/
  ├── package.json
  ├── .env                      # Environment variables
  ├── server.js                 # Main server file
  ├── config/
  │   └── db.js                 # MongoDB connection
  ├── models/
  │   ├── User.js               # User model
  │   └── Chat.js               # Chat model
  ├── routes/
  │   ├── auth.js               # Authentication routes
  │   └── chat.js               # Chat routes
  ├── middleware/
  │   └── auth.js               # Authentication middleware
  └── controllers/
      ├── authController.js     # Auth business logic
      └── chatController.js     # Chat business logic
```

## Milestone 2.2: Authentication Context & Services

**Goal**: Create the foundation for frontend authentication that connects to our MongoDB backend.

**Tasks**:

1. **Create Auth Service**:
   - Create `src/services/authService.js` for API interactions
   - Implement login, register, logout, and token refresh functions
   - Add password reset request functionality
   - Configure API base URL to connect to our backend

2. **Implement Auth Context**:
   - Create `src/context/AuthContext.js`
   - Implement user state management
   - Add login, logout, and registration methods
   - Create token storage and retrieval functions
   - Store user ID and other MongoDB-specific data

3. **Add JWT Utilities**:
   - Create helper functions to decode JWT tokens
   - Implement secure token storage in localStorage
   - Add functionality to include tokens in API requests

**Files to Create/Modify**:
```
src/
  ├── services/
  │   └── authService.js    # API calls to MongoDB backend
  ├── context/
  │   └── AuthContext.js    # Auth state provider
  └── utils/
      └── tokenUtils.js     # JWT handling utilities
```

## Milestone 2.3: Sign-Up Implementation

**Goal**: Implement user registration functionality connected to MongoDB.

**Tasks**:

1. **Create SignUp Form Components**:
   - Create reusable form input components
   - Implement form state management and validation
   - Add password strength indicator
   - Implement submit handling

2. **Update SignUp Page**:
   - Enhance existing placeholder page
   - Integrate form components
   - Add success/error handling
   - Implement email verification UI elements

3. **Add Sign-Up API Integration**:
   - Connect form submission to MongoDB through auth service
   - Handle API responses and errors
   - Implement redirect after successful registration

**Files to Create/Modify**:
```
src/
  ├── components/
  │   └── Auth/
  │       ├── SignUpForm.js         # Main signup form
  │       ├── PasswordStrength.js   # Password strength indicator
  │       └── FormInput.js          # Reusable form input
  └── pages/
      └── Auth/
          └── SignupPage.js         # Update existing page
```

## Milestone 2.4: Login Implementation

**Goal**: Implement user login functionality and session management with MongoDB.

**Tasks**:

1. **Create Login Form Components**:
   - Create login form with validation
   - Add "Remember me" functionality
   - Implement error handling for MongoDB authentication issues

2. **Update Login Page**:
   - Enhance existing placeholder page
   - Integrate form components
   - Add forgot password link
   - Implement authentication error handling

3. **Add Login API Integration**:
   - Connect form submission to MongoDB auth service
   - Handle authentication tokens
   - Store user info from MongoDB response
   - Implement automatic redirect to previous page

**Files to Create/Modify**:
```
src/
  ├── components/
  │   └── Auth/
  │       ├── LoginForm.js          # Main login form
  │       └── SocialLoginButtons.js # Optional social login
  └── pages/
      └── Auth/
          └── LoginPage.js          # Update existing page
```

## Milestone 2.5: Password Recovery Flow

**Goal**: Implement forgot password and reset functionality with MongoDB.

**Tasks**:

1. **Create Forgot Password Components**:
   - Create email entry form
   - Implement confirmation screens
   - Add validation and error handling

2. **Implement Password Reset Components**:
   - Create password reset form
   - Add token validation
   - Implement success/error handling

3. **Create New Pages**:
   - Add ForgotPasswordPage
   - Add ResetPasswordPage
   - Update routing configuration

**Files to Create/Modify**:
```
src/
  ├── components/
  │   └── Auth/
  │       ├── ForgotPasswordForm.js # Email form
  │       └── ResetPasswordForm.js  # New password form
  ├── pages/
  │   └── Auth/
  │       ├── ForgotPasswordPage.js # New page
  │       └── ResetPasswordPage.js  # New page
  └── App.js                        # Update routes
```

## Milestone 2.6: Protected Routes & User-Specific Chats

**Goal**: Implement route protection and user-specific chat functionality with MongoDB.

**Tasks**:

1. **Create Protected Route Component**:
   - Create HOC for route protection
   - Implement authentication checking against MongoDB tokens
   - Add redirect logic for unauthenticated users

2. **Update Routing Configuration**:
   - Integrate protected routes
   - Update navigation components
   - Add conditional rendering based on auth state

3. **Create User Profile Components**:
   - Add user avatar and display name component
   - Create simple profile page/modal with MongoDB user data
   - Implement logout functionality

4. **Implement User-Specific Chats**:
   - Create chat service that fetches user's chats from MongoDB
   - Implement chat history persistence
   - Add user ID to all chat-related requests

**Files to Create/Modify**:
```
src/
  ├── components/
  │   ├── Auth/
  │   │   ├── ProtectedRoute.js     # Route protection
  │   │   └── UserProfile.js        # User info display
  │   └── common/
  │       └── Navigation.js         # Update with auth state
  ├── pages/
  │   └── Auth/
  │       └── ProfilePage.js        # Basic profile page
  ├── services/
  │   └── chatService.js            # User-specific chat service
  └── App.js                        # Update routing
```

## Integration Testing

After implementing each sub-milestone:

1. Test MongoDB connection and data persistence
2. Test the individual components in isolation
3. Integrate with existing components and test
4. Test error scenarios and edge cases
5. Ensure responsive design on all device sizes
6. Verify user data is correctly stored and retrieved from MongoDB

## Best Practices

- Use environment variables for all sensitive MongoDB connection info
- Properly hash passwords before storing in MongoDB
- Implement proper error handling for all MongoDB operations
- Use Mongoose validation for data integrity
- Implement proper token refresh mechanisms
- Use consistent loading/error state UI patterns
- Follow accessibility guidelines for all forms
- Add form validation with helpful error messages

## Next Steps After Completion

Once the authentication system with MongoDB integration is complete, we'll be ready to move to Milestone 3 (Chatbot Interface), building on our user authentication to create personalized chat experiences that are stored in MongoDB for each user. 