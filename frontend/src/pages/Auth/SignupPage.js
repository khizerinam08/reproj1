import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';

const SignupPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Sign Up</h1>
          <p className="text-secondary mb-8 text-center">
            This feature will be implemented in Milestone 2. For now, this is a placeholder page.
          </p>
          <div className="text-center">
            <Link to="/login" className="text-primary hover:text-white">
              Already have an account? Login here
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage; 