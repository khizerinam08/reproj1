# Authentication Services

This directory contains services for interacting with the authentication API.

## Overview

`authService.js` provides functions to interact with the backend authentication API endpoints, including:
- User registration
- User login
- Password reset
- Profile management

## API Structure

The service connects to our MongoDB backend at `http://localhost:5000/api` by default.

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register a new user |
| `/auth/login` | POST | Log in a user |
| `/auth/profile` | GET | Get the user's profile (authenticated) |
| `/auth/forgot-password` | POST | Request a password reset |
| `/auth/reset-password` | POST | Reset a password with token |

## Implementation Details

### API Instance

The service uses Axios to communicate with the backend:

```javascript
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Authentication Token

Authentication tokens are automatically added to requests using an Axios interceptor:

```javascript
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
```

## Usage Examples

### Register a User

```javascript
import authService from '../services/authService';

const registerUser = async (userData) => {
  try {
    const response = await authService.register({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'Password123'
    });
    console.log('Registration successful!', response);
  } catch (error) {
    console.error('Registration failed:', error.message);
  }
};
```

### Login a User

```javascript
import authService from '../services/authService';

const loginUser = async (credentials) => {
  try {
    const response = await authService.login({
      email: 'john@example.com',
      password: 'Password123'
    });
    console.log('Login successful!', response);
  } catch (error) {
    console.error('Login failed:', error.message);
  }
};
```

### Get User Profile

```javascript
import authService from '../services/authService';

const getUserProfile = async () => {
  try {
    const profile = await authService.getUserProfile();
    console.log('User profile:', profile);
  } catch (error) {
    console.error('Failed to get profile:', error.message);
  }
};
```

## Error Handling

All service methods include standardized error handling:

```javascript
try {
  // API call
} catch (error) {
  throw handleApiError(error);
}
```

The `handleApiError` function extracts error messages from the API response:

```javascript
const handleApiError = (error) => {
  const message = 
    error.response?.data?.message || 
    error.message || 
    'Something went wrong';
  
  const formattedError = new Error(message);
  formattedError.status = error.response?.status;
  
  return formattedError;
};
``` 