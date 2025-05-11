import axios from 'axios';
import { getToken } from '../utils/tokenUtils';

// API base URL - configure to point to our backend
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor to add auth token to requests
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

/**
 * Register a new user
 * @param {Object} userData - User registration data (name, email, password)
 * @returns {Promise} Promise with user data and token
 */
export const register = async (userData) => {
  try {
    const response = await api.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Login a user
 * @param {Object} credentials - Login credentials (email, password)
 * @returns {Promise} Promise with user data and token
 */
export const login = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Get current user profile
 * @returns {Promise} Promise with user profile data
 */
export const getUserProfile = async () => {
  try {
    const response = await api.get('/auth/profile');
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Request password reset
 * @param {string} email - User's email
 * @returns {Promise} Promise with message
 */
export const requestPasswordReset = async (email) => {
  try {
    const response = await api.post('/auth/forgot-password', { email });
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Reset password
 * @param {string} token - Reset token
 * @param {string} password - New password
 * @returns {Promise} Promise with message
 */
export const resetPassword = async (token, password) => {
  try {
    const response = await api.post('/auth/reset-password', { token, password });
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Handle API error responses
 * @param {Error} error - Axios error object
 * @returns {Error} Formatted error with message
 */
const handleApiError = (error) => {
  // Extract the error message from the API response if it exists
  const message = 
    error.response?.data?.message || 
    error.message || 
    'Something went wrong';
    
  const status = error.response?.status;
  
  // Create a new error with the message
  const formattedError = new Error(message);
  formattedError.status = status;
  
  return formattedError;
};

export default {
  register,
  login,
  getUserProfile,
  requestPasswordReset,
  resetPassword
}; 