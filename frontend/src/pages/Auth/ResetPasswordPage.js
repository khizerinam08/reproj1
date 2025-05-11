import React, { useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';
import ResetPasswordForm from '../../components/Auth/ResetPasswordForm';

const ResetPasswordPage = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  
  // Use useEffect at the top level, not conditionally
  useEffect(() => {
    // If no token is provided, redirect to forgot password page
    if (!token) {
      navigate('/forgot-password');
    }
  }, [navigate, token]);
  
  // If no token, render nothing while the redirect happens
  if (!token) {
    return null;
  }
  
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-gray-900 rounded-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center">Reset Password</h1>
          <p className="text-gray-400 mb-8 text-center">
            Create a new password for your account. Make sure it's secure.
          </p>
          
          {/* Reset Password Form */}
          <ResetPasswordForm token={token} />
          
          {/* Back to Login Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Remember your password?{' '}
              <Link to="/login" className="text-[#bc2424] hover:text-white">
                Back to login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ResetPasswordPage; 