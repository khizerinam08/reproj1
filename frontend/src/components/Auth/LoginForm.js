import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, useLocation, Link } from 'react-router-dom';
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
  password: yup
    .string()
    .required('Password is required'),
  rememberMe: yup.boolean(),
});

/**
 * LoginForm component for user authentication
 */
const LoginForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    mode: 'onBlur',
  });
  
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');
  
  // Get the redirect path from location state or default to /chatbot
  const from = location.state?.from?.pathname || '/chatbot';
  
  // Handle form submission
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setApiError('');
    
    try {
      // Login the user through the auth context
      const loginData = {
        email: data.email,
        password: data.password,
      };
      
      await login(loginData);
      
      // Navigate to the redirect path
      navigate(from, { replace: true });
    } catch (error) {
      setApiError(error.message || 'Invalid email or password. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="w-full max-w-md">
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
          placeholder="Enter your password"
          register={register}
          errors={errors}
          required
          autoComplete="current-password"
        />
        
        {/* Remember me and Forgot password */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="rememberMe"
              type="checkbox"
              className="h-4 w-4 bg-gray-800 border-gray-600 rounded focus:ring-[#bc2424]"
              {...register('rememberMe')}
            />
            <label htmlFor="rememberMe" className="ml-2 block text-sm text-gray-300">
              Remember me
            </label>
          </div>
          
          <div className="text-sm">
            <Link to="/forgot-password" className="text-[#bc2424] hover:text-white">
              Forgot password?
            </Link>
          </div>
        </div>
        
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
            {isSubmitting ? 'Signing In...' : 'Sign In'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LoginForm; 