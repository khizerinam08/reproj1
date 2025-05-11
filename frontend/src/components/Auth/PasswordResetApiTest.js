import React, { useState } from 'react';
import axios from 'axios';

/**
 * Test component for password reset API connectivity
 * This is for development/testing only
 */
const PasswordResetApiTest = () => {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState([]);
  const [testEmail, setTestEmail] = useState('');
  
  const runTest = async () => {
    if (!testEmail) {
      setResults(['Please enter a test email address']);
      return;
    }
    
    setTesting(true);
    setResults([]);
    
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
    const logs = [];
    
    // Log function to capture results
    const log = (message) => {
      logs.push(message);
      setResults([...logs]);
    };
    
    try {
      log(`🔍 Testing password reset flow with API at: ${API_URL}`);
      log(`📧 Using email: ${testEmail}`);
      
      // Test forgot password endpoint
      log('Step 1: Testing forgot password request...');
      try {
        const response = await axios.post(`${API_URL}/auth/forgot-password`, {
          email: testEmail
        });
        log(`✅ Password reset request successful! ${response.data.message || ''}`);
        
        if (response.data.mockToken) {
          log(`ℹ️ Mock token received for testing: ${response.data.mockToken.substring(0, 10)}...`);
          
          // Test reset password endpoint with the mock token
          log('Step 2: Testing password reset with token...');
          try {
            const resetResponse = await axios.post(`${API_URL}/auth/reset-password`, {
              token: response.data.mockToken,
              password: 'NewPassword123'
            });
            log(`✅ Password reset successful! ${resetResponse.data.message || ''}`);
          } catch (error) {
            log(`❌ Password reset failed: ${error.response?.data?.message || error.message}`);
          }
        } else {
          log('⚠️ No mock token received, skipping password reset test');
        }
      } catch (error) {
        if (error.response?.status === 404) {
          log('⚠️ Forgot password endpoint not implemented yet');
        } else {
          log(`❌ Forgot password request failed: ${error.response?.data?.message || error.message}`);
        }
      }
      
      log('✅ Password reset flow test completed!');
    } catch (error) {
      log(`❌ Test failed: ${error.message}`);
    } finally {
      setTesting(false);
    }
  };
  
  return (
    <div className="mt-8 border border-gray-700 rounded-md p-4">
      <h3 className="text-lg font-medium mb-2">Password Reset API Test</h3>
      <p className="text-sm text-gray-400 mb-4">
        This tool tests the password reset API endpoints.
      </p>
      
      <div className="mb-4">
        <label htmlFor="testEmail" className="block text-sm font-medium text-gray-200 mb-1">
          Test Email
        </label>
        <input
          id="testEmail"
          type="email"
          value={testEmail}
          onChange={(e) => setTestEmail(e.target.value)}
          placeholder="Enter test email address"
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md"
        />
      </div>
      
      <button
        onClick={runTest}
        disabled={testing || !testEmail}
        className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 
          focus:outline-none focus:ring-2 focus:ring-gray-500
          disabled:opacity-50 disabled:cursor-not-allowed mr-2"
      >
        {testing ? 'Testing...' : 'Run API Test'}
      </button>
      
      {results.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-medium mb-2">Test Results:</h4>
          <div className="bg-black bg-opacity-40 p-3 rounded-md overflow-auto max-h-[300px] text-xs font-mono">
            {results.map((result, index) => (
              <div key={index} className={`mb-1 ${
                result.startsWith('❌') ? 'text-red-400' : 
                result.includes('✅') ? 'text-green-400' : 'text-gray-300'
              }`}>
                {result}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PasswordResetApiTest; 