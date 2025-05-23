import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';
import SignUpForm from '../../components/Auth/SignUpForm';
import SignUpApiTest from '../../components/Auth/SignUpApiTest';

// Toggle development features
const isDevelopment = process.env.NODE_ENV === 'development';

const SignupPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Create Account</h1>
          <p className="text-gray-400 mb-8 text-center">
            Join our community to predict and prevent crime in your area.
          </p>
          
          {/* SignUp Form */}
          <SignUpForm />
          
          {/* Login Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Already have an account?{' '}
              <Link to="/login" className="text-[#bc2424] hover:text-white">
                Login here
              </Link>
            </p>
          </div>
          
          {/* Development Tools - only shown in development mode */}
          {isDevelopment && <SignUpApiTest />}
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage; 