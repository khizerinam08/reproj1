/**
 * MongoDB Authentication Test Script
 * This script tests the basic functionality of our authentication API
 * Run with: node test.js
 */

const axios = require('axios');

// Base URL for API
const API_URL = 'http://localhost:5000/api';

// Test user data
const testUser = {
  name: 'Test User',
  email: `test${Date.now()}@example.com`, // Unique email to avoid conflicts
  password: 'password123'
};

// Store the auth token and user ID
let authToken;
let userId;
let chatId;

// Function to log test results
const logTest = (testName, success, data = null, error = null) => {
  console.log(`\n----- ${testName} -----`);
  if (success) {
    console.log('✅ PASSED');
    if (data) console.log('Data:', data);
  } else {
    console.log('❌ FAILED');
    if (error) console.log('Error:', error);
  }
};

// Run all tests
const runTests = async () => {
  try {
    // Test 1: Register new user
    try {
      console.log('\n🔍 Testing User Registration...');
      const registerResponse = await axios.post(`${API_URL}/auth/register`, testUser);
      authToken = registerResponse.data.token;
      userId = registerResponse.data._id;
      logTest('Register User', true, { userId, email: registerResponse.data.email });
    } catch (error) {
      logTest('Register User', false, null, error.response?.data || error.message);
      process.exit(1);
    }

    // Test 2: Login user
    try {
      console.log('\n🔍 Testing User Login...');
      const loginResponse = await axios.post(`${API_URL}/auth/login`, {
        email: testUser.email,
        password: testUser.password
      });
      authToken = loginResponse.data.token;
      logTest('Login User', true, { token: authToken.substring(0, 15) + '...' });
    } catch (error) {
      logTest('Login User', false, null, error.response?.data || error.message);
    }

    // Test 3: Get user profile (authenticated request)
    try {
      console.log('\n🔍 Testing Profile Access...');
      const profileResponse = await axios.get(`${API_URL}/auth/profile`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      logTest('Get User Profile', true, profileResponse.data);
    } catch (error) {
      logTest('Get User Profile', false, null, error.response?.data || error.message);
    }

    // Test 4: Create a new chat
    try {
      console.log('\n🔍 Testing Chat Creation...');
      const chatResponse = await axios.post(
        `${API_URL}/chats`, 
        {
          title: 'Test Chat',
          initialMessage: 'Hello, this is a test message'
        },
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      );
      chatId = chatResponse.data._id;
      logTest('Create Chat', true, { chatId, title: chatResponse.data.title });
    } catch (error) {
      logTest('Create Chat', false, null, error.response?.data || error.message);
    }

    // Test 5: Add message to chat
    try {
      console.log('\n🔍 Testing Adding Message to Chat...');
      const messageResponse = await axios.post(
        `${API_URL}/chats/${chatId}/messages`,
        {
          sender: 'user',
          content: 'This is another test message'
        },
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      );
      logTest('Add Message', true, { 
        messageCount: messageResponse.data.messages.length,
        lastMessage: messageResponse.data.messages[messageResponse.data.messages.length - 1]
      });
    } catch (error) {
      logTest('Add Message', false, null, error.response?.data || error.message);
    }

    // Test 6: Get all user chats
    try {
      console.log('\n🔍 Testing Retrieving User Chats...');
      const chatsResponse = await axios.get(
        `${API_URL}/chats`,
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      );
      logTest('Get User Chats', true, { chatCount: chatsResponse.data.length });
    } catch (error) {
      logTest('Get User Chats', false, null, error.response?.data || error.message);
    }

    console.log('\n✨ All tests completed! ✨');
  } catch (error) {
    console.error('Test runner error:', error);
  }
};

// Check if MongoDB server is running first
console.log('🚀 Starting MongoDB Authentication API Tests...');
console.log('⚠️  Make sure your server is running at http://localhost:5000');
console.log('⚠️  Make sure MongoDB is running');

runTests(); 