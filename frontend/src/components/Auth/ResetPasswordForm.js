import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useAuth } from '../../context/AuthContext';
import FormInput from './FormInput';
import PasswordStrength from './PasswordStrength';

// Validation schema
const schema = yup.object().shape({
  password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\W]{8,}$/,
      'Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number'
    ),
  confirmPassword: yup
    .string()
    .required('Please confirm your password')
    .oneOf([yup.ref('password'), null], 'Passwords must match'),
});

/**
 * ResetPasswordForm component for setting a new password
 */
const ResetPasswordForm = ({ token }) => {
  const { register, handleSubmit, formState: { errors }, watch } = useForm({
    resolver: yupResolver(schema),
    mode: 'onChange',
  });
  
  const navigate = useNavigate();
  const { resetPassword } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');
  const [resetSuccess, setResetSuccess] = useState(false);
  
  // Watch the password field for strength meter
  const watchPassword = watch('password', '');
  
  // Handle form submission
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setApiError('');
    
    try {
      // Reset password through auth context
      await resetPassword(token, data.password);
      
      // Show success message
      setResetSuccess(true);
      
      // Redirect to login after successful reset
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setApiError(error.message || 'An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="w-full max-w-md">
      {/* Success message */}
      {resetSuccess ? (
        <div className="bg-green-500 bg-opacity-20 border border-green-500 text-green-300 px-4 py-3 rounded mb-4">
          <h3 className="text-lg font-medium mb-1">Password Reset Successful!</h3>
          <p>Your password has been updated. You will be redirected to the login page shortly.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* API Error display */}
          {apiError && (
            <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded mb-4">
              <p>{apiError}</p>
            </div>
          )}
          
          {/* Password field */}
          <FormInput
            id="password"
            name="password"
            label="New Password"
            type="password"
            placeholder="Create a new password"
            register={register}
            errors={errors}
            required
            autoComplete="new-password"
          />
          
          {/* Password strength meter */}
          <PasswordStrength password={watchPassword} />
          
          {/* Confirm Password field */}
          <FormInput
            id="confirmPassword"
            name="confirmPassword"
            label="Confirm Password"
            type="password"
            placeholder="Confirm your new password"
            register={register}
            errors={errors}
            required
            autoComplete="new-password"
          />
          
          {/* Submit button */}
          <div className="mt-6">
            <button
              type="submit"
              disabled={isSubmitting}
              className={`
                w-full py-3 px-4 bg-[#bc2424] text-white font-semibold rounded-md
                hover:bg-[#a01d1d] focus:outline-none focus:ring-2 focus:ring-[#bc2424]
                ${isSubmitting ? 'opacity-70 cursor-not-allowed' : ''}
              `}
            >
              {isSubmitting ? 'Resetting Password...' : 'Reset Password'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default ResetPasswordForm; 