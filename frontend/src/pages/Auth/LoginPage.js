import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';
import LoginForm from '../../components/Auth/LoginForm';
import LoginApiTest from '../../components/Auth/LoginApiTest';

// Toggle development features
const isDevelopment = process.env.NODE_ENV === 'development';

const LoginPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Sign In</h1>
          <p className="text-gray-400 mb-8 text-center">
            Sign in to access your account and stay secure.
          </p>
          
          {/* Login Form */}
          <LoginForm />
          
          {/* SignUp Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Don't have an account?{' '}
              <Link to="/signup" className="text-[#bc2424] hover:text-white">
                Create an account
              </Link>
            </p>
          </div>
          
          {/* Development Tools - only shown in development mode */}
          {isDevelopment && <LoginApiTest />}
        </div>
      </div>
    </Layout>
  );
};

export default LoginPage; 