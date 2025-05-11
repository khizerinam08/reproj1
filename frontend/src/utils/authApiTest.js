import axios from 'axios';

/**
 * Test utility for authentication flow
 * This will verify the connection to the backend API and test auth endpoints
 */
export const testAuthApi = async () => {
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
    let loginResponse = null;
    try {
      loginResponse = await axios.post(`${API_URL}/auth/login`, {
        email: testUser.email,
        password: testUser.password,
      });
      console.log(`✅ Login successful! Token received: ${loginResponse.data.token ? 'Yes' : 'No'}`);
    } catch (error) {
      console.error(`❌ Login failed: ${error.response?.data?.message || error.message}`);
      throw error;
    }
    
    // 4. Test profile retrieval (if login was successful)
    console.log('Step 4: Testing profile retrieval...');
    try {
      // Get the token from the login response
      const token = loginResponse?.data?.token;
      if (token) {
        const profileResponse = await axios.get(`${API_URL}/auth/profile`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        console.log(`✅ Profile retrieval successful! User: ${profileResponse.data.name || 'Unknown'}`);
      } else {
        console.log('⚠️ Skipping profile test - no token available');
      }
    } catch (error) {
      console.error(`❌ Profile retrieval failed: ${error.response?.data?.message || error.message}`);
    }
    
    console.log('✅ Authentication flow test completed!');
    return true;
  } catch (error) {
    console.error(`❌ Test failed: ${error.message}`);
    return false;
  }
}; 