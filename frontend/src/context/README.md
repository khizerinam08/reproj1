# Authentication Context

This directory contains the authentication context which provides authentication functionality throughout the application.

## Overview

`AuthContext.js` implements a React Context that manages:
- User authentication state
- Login functionality
- Registration functionality
- Password reset functionality
- Protected routes

## How to Use

### 1. Wrap your application with AuthProvider

The `AuthProvider` is already set up in `App.js`:

```jsx
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      {/* your app components */}
    </AuthProvider>
  );
}
```

### 2. Use the authentication hook in components

```jsx
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { user, login, register, logout, loading, error } = useAuth();

  // Example login handler
  const handleLogin = async (email, password) => {
    try {
      await login({ email, password });
      // Redirect or show success message
    } catch (error) {
      // Handle error
    }
  };

  // Check if user is logged in
  if (user) {
    return <div>Welcome, {user.name}!</div>;
  }

  return <div>Please log in</div>;
}
```

### 3. Protect Routes

Use the `ProtectedRoute` component to guard routes that require authentication:

```jsx
import ProtectedRoute from './components/Auth/ProtectedRoute';

<Route 
  path="/secure-page" 
  element={
    <ProtectedRoute>
      <SecurePage />
    </ProtectedRoute>
  } 
/>
```

## Available Methods

- `login({ email, password })` - Log in a user
- `register({ name, email, password })` - Register a new user
- `logout()` - Log out the current user
- `requestPasswordReset(email)` - Request a password reset link
- `resetPassword(token, password)` - Reset password with token
- `isAuthenticated()` - Check if user is authenticated
- `getUserId()` - Get the current user's ID

## Authentication Flow

1. **User Registration**: Creates a new user in MongoDB
2. **User Login**: Authenticates and receives a JWT token
3. **Token Storage**: Token is stored in localStorage
4. **Authentication Check**: Protected routes verify authentication
5. **Profile Loading**: User profile is loaded when authenticated
6. **Logout**: Removes token and user data

## Testing Authentication

You can test the authentication flow using the utility in `utils/authTestUtils.js`:

```jsx
import { testAuthFlow } from '../utils/authTestUtils';

// In a component or console
testAuthFlow().then(() => {
  console.log('Authentication test complete');
});
``` 