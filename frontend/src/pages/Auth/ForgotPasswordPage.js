import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';
import ForgotPasswordForm from '../../components/Auth/ForgotPasswordForm';
import PasswordResetApiTest from '../../components/Auth/PasswordResetApiTest';

// Toggle development features
const isDevelopment = process.env.NODE_ENV === 'development';

const ForgotPasswordPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Forgot Password</h1>
          <p className="text-gray-400 mb-8 text-center">
            Enter your email address and we'll send you instructions to reset your password.
          </p>
          
          {/* Forgot Password Form */}
          <ForgotPasswordForm />
          
          {/* Back to Login Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Remember your password?{' '}
              <Link to="/login" className="text-[#bc2424] hover:text-white">
                Back to login
              </Link>
            </p>
          </div>
          
          {/* Development Tools - only shown in development mode */}
          {isDevelopment && <PasswordResetApiTest />}
        </div>
      </div>
    </Layout>
  );
};

export default ForgotPasswordPage; 