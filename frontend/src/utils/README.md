# Authentication Utilities

This directory contains utility functions for the authentication system.

## Overview

### `tokenUtils.js`

Provides functions for working with JWT authentication tokens:
- Storing and retrieving tokens from localStorage
- Parsing token payloads
- Validating token expiration
- Extracting user information from tokens

### `authTestUtils.js`

Provides testing utilities for the authentication system:
- Testing the complete authentication flow
- Verifying connectivity with the backend

## Token Utilities

### Storage Functions

```javascript
// Store token in localStorage
setToken(token);

// Get token from localStorage
const token = getToken();

// Remove token from localStorage
removeToken();

// Check if token exists
const hasAuthToken = hasToken();
```

### Token Parsing and Validation

```javascript
// Parse JWT token to get payload
const payload = parseToken(token);

// Check if token is expired
const expired = isTokenExpired(token);

// Get user ID from token
const userId = getUserIdFromToken(token);
```

## Token Structure

The JWT tokens from our backend have the following structure:

```javascript
{
  "id": "user_id_from_mongodb",
  "iat": 1619794513,  // Issued at timestamp
  "exp": 1619880913   // Expiration timestamp
}
```

## Authentication Test Utilities

The `testAuthFlow()` function in `authTestUtils.js` tests the full authentication flow:

1. Registers a new user with a unique email
2. Logs in with the new user credentials
3. Retrieves the user profile
4. Reports success/failure for each step

Example usage:

```javascript
import { testAuthFlow } from './utils/authTestUtils';

// Run the test
testAuthFlow()
  .then(() => console.log('Test completed'))
  .catch(err => console.error('Test failed:', err));
```

## Security Notes

- Tokens are stored in localStorage, which is accessible by JavaScript in the same domain
- For production, consider implementing CSRF protection and shorter token lifetimes
- Always transmit tokens over HTTPS
- Consider adding token refresh mechanisms for longer sessions 