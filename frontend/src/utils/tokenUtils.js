/**
 * Utility functions for handling JWT tokens
 */

// Store token in localStorage
export const setToken = (token) => {
  localStorage.setItem('authToken', token);
};

// Get token from localStorage
export const getToken = () => {
  return localStorage.getItem('authToken');
};

// Remove token from localStorage
export const removeToken = () => {
  localStorage.removeItem('authToken');
};

// Check if token exists
export const hasToken = () => {
  return !!getToken();
};

// Parse JWT token to get payload (without library dependency)
export const parseToken = (token) => {
  if (!token) return null;
  
  try {
    // Split the token and get the payload part
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // Decode the payload
    const payload = JSON.parse(
      decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )
    );
    
    return payload;
  } catch (error) {
    console.error('Invalid token', error);
    return null;
  }
};

// Check if token is expired
export const isTokenExpired = (token) => {
  const payload = parseToken(token);
  if (!payload) return true;
  
  // Get expiration time from token
  const expirationTime = payload.exp * 1000; // Convert to milliseconds
  const currentTime = Date.now();
  
  return currentTime > expirationTime;
};

// Get user ID from token
export const getUserIdFromToken = (token) => {
  const payload = parseToken(token);
  return payload ? payload.id : null;
}; 