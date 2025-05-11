/**
 * Utility functions for testing the authentication system
 */

import axios from 'axios';
import { getToken, setToken, removeToken } from './tokenUtils';

/**
 * Test utility for authentication flow
 * This will verify the connection to the backend API and test auth endpoints
 */
export const testAuthFlow = async () => {
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
  
  // Generate a unique test user
  const timestamp = new Date().getTime();
  const testUser = {
    name: `Test User ${timestamp}`,
    email: `testuser${timestamp}@example.com`,
    password: 'Test1234!',
  };
  
  console.log(`🔍 Testing authentication flow with API at: ${API_URL}`);
  console.log(`📝 Using test credentials: ${testUser.email} / ${testUser.password.slice(0, 3)}*** (partially hidden)`);
  
  try {
    // 1. Test API connection
    console.log('Step 1: Testing API connection...');
    await axios.get(`${API_URL}/health`).catch(error => {
      // If health endpoint doesn't exist, we'll just log and continue
      console.log('⚠️ Health check endpoint not available, continuing with auth tests');
    });
    
    // 2. Test registration
    console.log('Step 2: Testing user registration...');
    let registerResponse;
    try {
      registerResponse = await axios.post(`${API_URL}/auth/register`, testUser);
      console.log(`✅ Registration successful! User ID: ${registerResponse.data.user?._id || 'ID not returned'}`);
    } catch (error) {
      console.error(`❌ Registration failed: ${error.response?.data?.message || error.message}`);
      if (error.response?.status === 400 && error.response?.data?.message.includes('already exists')) {
        console.log('⚠️ User with this email might already exist. Continuing to login test.');
      } else {
        throw error;
      }
    }
    
    // 3. Test login
    console.log('Step 3: Testing user login...');
    try {
      const loginResponse = await axios.post(`${API_URL}/auth/login`, {
        email: testUser.email,
        password: testUser.password,
      });
      console.log(`✅ Login successful! Token received: ${loginResponse.data.token ? 'Yes' : 'No'}`);
    } catch (error) {
      console.error(`❌ Login failed: ${error.response?.data?.message || error.message}`);
      throw error;
    }
    
    // 4. Test password reset request (optional, will only check endpoint existence)
    console.log('Step 4: Testing password reset request flow...');
    try {
      const forgotResponse = await axios.post(`${API_URL}/auth/forgot-password`, {
        email: testUser.email,
      });
      console.log('✅ Password reset request endpoint working');
      
      // Check if we got a mock token for testing
      if (forgotResponse.data.mockToken) {
        console.log('✅ Mock token received for testing');
        
        // Test reset password endpoint with the mock token
        try {
          const resetResponse = await axios.post(`${API_URL}/auth/reset-password`, {
            token: forgotResponse.data.mockToken,
            password: 'NewTest1234!'
          });
          console.log('✅ Password reset endpoint working');
        } catch (resetError) {
          console.error(`❌ Password reset failed: ${resetError.response?.data?.message || resetError.message}`);
        }
      }
    } catch (error) {
      if (error.response?.status === 404) {
        console.log('⚠️ Password reset endpoint not implemented yet');
      } else {
        console.error(`❌ Password reset request failed: ${error.response?.data?.message || error.message}`);
      }
    }
    
    console.log('✅ Authentication flow test completed successfully!');
    return true;
  } catch (error) {
    console.error(`❌ Test failed: ${error.message}`);
    return false;
  }
};

export default {
  testAuthFlow
}; 