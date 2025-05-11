import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  setToken, 
  getToken, 
  removeToken, 
  hasToken, 
  isTokenExpired,
  getUserIdFromToken
} from '../utils/tokenUtils';
import authService from '../services/authService';

// Create context
const AuthContext = createContext();

// Provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check for existing token and load user on mount
  useEffect(() => {
    const initializeAuth = async () => {
      if (hasToken()) {
        const token = getToken();
        
        // Check if token is expired
        if (isTokenExpired(token)) {
          handleLogout();
          setLoading(false);
          return;
        }
        
        try {
          // Fetch user profile
          const userData = await authService.getUserProfile();
          setUser(userData);
        } catch (error) {
          console.error('Error loading user:', error);
          handleLogout();
        }
      }
      
      setLoading(false);
    };

    initializeAuth();
  }, []);

  // Register new user
  const register = async (userData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authService.register(userData);
      
      // Store the token and set user data
      if (response && response.token) {
        setToken(response.token);
        setUser(response);
      } else {
        console.error('No token received in register response');
      }
      
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Login user
  const login = async (credentials) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authService.login(credentials);
      
      // Store the token and set user data
      if (response && response.token) {
        setToken(response.token);
        setUser(response);
      } else {
        console.error('No token received in login response');
      }
      
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout user
  const handleLogout = () => {
    removeToken();
    setUser(null);
  };

  // Request password reset
  const requestPasswordReset = async (email) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authService.requestPasswordReset(email);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Reset password
  const resetPassword = async (token, password) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authService.resetPassword(token, password);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Get user ID
  const getUserId = () => {
    if (user && user._id) {
      return user._id;
    }
    
    const token = getToken();
    if (token) {
      return getUserIdFromToken(token);
    }
    
    return null;
  };

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!user;
  };

  // Context value
  const value = {
    user,
    loading,
    error,
    register,
    login,
    logout: handleLogout,
    requestPasswordReset,
    resetPassword,
    getUserId,
    isAuthenticated
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default AuthContext; 