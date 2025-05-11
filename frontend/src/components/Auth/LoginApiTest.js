import React, { useState } from 'react';
import { testAuthApi } from '../../utils/authApiTest';

/**
 * Test component for API connectivity for login
 * This is for development/testing only
 */
const LoginApiTest = () => {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState([]);
  
  const runTest = async () => {
    setTesting(true);
    setResults([]);
    
    // Create a logging function to capture results
    const captureLog = (message) => {
      setResults(prev => [...prev, message]);
    };
    
    try {
      // Replace console.log with our capture function
      const originalConsoleLog = console.log;
      const originalConsoleError = console.error;
      
      console.log = captureLog;
      console.error = (message) => captureLog(`ERROR: ${message}`);
      
      // Run the test
      await testAuthApi();
      
      // Restore original console functions
      console.log = originalConsoleLog;
      console.error = originalConsoleError;
    } catch (error) {
      setResults(prev => [...prev, `Test failed: ${error.message}`]);
    } finally {
      setTesting(false);
    }
  };
  
  return (
    <div className="mt-8 border border-gray-700 rounded-md p-4">
      <h3 className="text-lg font-medium mb-2">API Connectivity Test</h3>
      <p className="text-sm text-gray-400 mb-4">
        This tool tests the connection to the authentication backend and verifies the login flow.
      </p>
      
      <button
        onClick={runTest}
        disabled={testing}
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
                result.startsWith('ERROR') ? 'text-red-400' : 
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

export default LoginApiTest; 