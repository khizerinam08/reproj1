import React from 'react';

/**
 * Reusable form input component with validation
 */
const FormInput = ({
  id,
  name,
  label,
  type = 'text',
  placeholder = '',
  register,
  errors,
  autoComplete = 'on',
  className = '',
  required = false,
  disabled = false,
}) => {
  return (
    <div className="mb-4">
      {label && (
        <label 
          htmlFor={id} 
          className="block text-sm font-medium text-gray-200 mb-1"
        >
          {label}
          {required && <span className="text-[#bc2424] ml-1">*</span>}
        </label>
      )}
      
      <input
        id={id}
        type={type}
        placeholder={placeholder}
        autoComplete={autoComplete}
        disabled={disabled}
        className={`
          w-full px-3 py-3 bg-gray-800 border rounded-md 
          focus:outline-none focus:ring-2 focus:ring-[#bc2424]
          ${errors && errors[name] ? 'border-red-500' : 'border-gray-700'}
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          ${className}
        `}
        {...(register && register(name))}
      />
      
      {errors && errors[name] && (
        <p className="mt-1 text-sm text-red-500">
          {errors[name]?.message}
        </p>
      )}
    </div>
  );
};

export default FormInput; 