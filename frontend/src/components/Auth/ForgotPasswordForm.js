import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useAuth } from '../../context/AuthContext';
import FormInput from './FormInput';

// Validation schema
const schema = yup.object().shape({
  email: yup
    .string()
    .required('Email is required')
    .email('Please enter a valid email address'),
});

/**
 * ForgotPasswordForm component for requesting a password reset
 */
const ForgotPasswordForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    mode: 'onBlur',
  });
  
  const { requestPasswordReset } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');
  const [resetSent, setResetSent] = useState(false);
  const [emailSent, setEmailSent] = useState('');
  
  // Handle form submission
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setApiError('');
    
    try {
      // Request password reset through auth context
      await requestPasswordReset(data.email);
      
      // Show success message
      setResetSent(true);
      setEmailSent(data.email);
    } catch (error) {
      setApiError(error.message || 'An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="w-full max-w-md">
      {/* Success message */}
      {resetSent ? (
        <div className="bg-green-500 bg-opacity-20 border border-green-500 text-green-300 px-4 py-3 rounded mb-4">
          <h3 className="text-lg font-medium mb-1">Reset Email Sent</h3>
          <p>We've sent recovery instructions to <strong>{emailSent}</strong>. Please check your email inbox.</p>
          <p className="mt-2 text-sm">
            If you don't see the email, check your spam folder. The link will expire in 1 hour.
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* API Error display */}
          {apiError && (
            <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded mb-4">
              <p>{apiError}</p>
            </div>
          )}
          
          {/* Email field */}
          <FormInput
            id="email"
            name="email"
            label="Email Address"
            type="email"
            placeholder="Enter your registered email address"
            register={register}
            errors={errors}
            required
            autoComplete="email"
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
              {isSubmitting ? 'Sending...' : 'Send Reset Instructions'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default ForgotPasswordForm; 