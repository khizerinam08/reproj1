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
  name: yup
    .string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must not exceed 50 characters'),
  email: yup
    .string()
    .required('Email is required')
    .email('Please enter a valid email address'),
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
 * SignUpForm component for user registration
 */
const SignUpForm = () => {
  const { register, handleSubmit, formState: { errors }, watch, reset } = useForm({
    resolver: yupResolver(schema),
    mode: 'onChange',
  });
  
  const navigate = useNavigate();
  const { register: registerUser } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');
  const [signupSuccess, setSignupSuccess] = useState(false);
  
  // Watch the password field for strength meter
  const watchPassword = watch('password', '');
  
  // Handle form submission
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setApiError('');
    
    try {
      // Register the user through the auth context
      const userData = {
        name: data.name,
        email: data.email,
        password: data.password,
      };
      
      await registerUser(userData);
      
      // Show success message
      setSignupSuccess(true);
      
      // Reset form
      reset();
      
      // Redirect to chatbot after successful registration
      setTimeout(() => {
        navigate('/chatbot');
      }, 2000);
    } catch (error) {
      setApiError(error.message || 'An error occurred during registration. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="w-full max-w-md">
      {/* Success message */}
      {signupSuccess ? (
        <div className="bg-green-500 bg-opacity-20 border border-green-500 text-green-300 px-4 py-3 rounded mb-4">
          <h3 className="text-lg font-medium mb-1">Registration Successful!</h3>
          <p>You've been successfully registered and logged in. Redirecting to the chatbot...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* API Error display */}
          {apiError && (
            <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded mb-4">
              <p>{apiError}</p>
            </div>
          )}
          
          {/* Name field */}
          <FormInput
            id="name"
            name="name"
            label="Full Name"
            type="text"
            placeholder="Enter your full name"
            register={register}
            errors={errors}
            required
            autoComplete="name"
          />
          
          {/* Email field */}
          <FormInput
            id="email"
            name="email"
            label="Email Address"
            type="email"
            placeholder="Enter your email address"
            register={register}
            errors={errors}
            required
            autoComplete="email"
          />
          
          {/* Password field */}
          <FormInput
            id="password"
            name="password"
            label="Password"
            type="password"
            placeholder="Create a password"
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
            placeholder="Confirm your password"
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
              {isSubmitting ? 'Creating Account...' : 'Create Account'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default SignUpForm;

 