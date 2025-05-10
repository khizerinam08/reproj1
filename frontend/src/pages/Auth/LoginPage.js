import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';

const LoginPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Login</h1>
          <p className="text-secondary mb-8 text-center">
            This feature will be implemented in Milestone 2. For now, this is a placeholder page.
          </p>
          <div className="text-center">
            <Link to="/signup" className="text-primary hover:text-white">
              Don't have an account? Sign up here
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default LoginPage; 