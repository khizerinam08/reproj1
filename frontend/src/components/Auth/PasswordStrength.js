import React, { useEffect, useState } from 'react';

/**
 * Password strength indicator component
 * Shows visual feedback about password strength
 */
const PasswordStrength = ({ password }) => {
  const [strength, setStrength] = useState({
    score: 0,
    label: 'Too Weak',
    color: 'bg-red-500',
  });

  // Calculate password strength
  useEffect(() => {
    if (!password) {
      setStrength({
        score: 0,
        label: 'Too Weak',
        color: 'bg-red-500',
      });
      return;
    }

    let score = 0;

    // Length check
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;

    // Character variety checks
    if (/[A-Z]/.test(password)) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;

    // Normalize score to 0-4 range
    score = Math.min(4, Math.floor(score / 1.5));

    // Set strength based on score
    const strengths = [
      { score: 0, label: 'Too Weak', color: 'bg-red-500' },
      { score: 1, label: 'Weak', color: 'bg-orange-500' },
      { score: 2, label: 'Fair', color: 'bg-yellow-400' },
      { score: 3, label: 'Good', color: 'bg-blue-500' },
      { score: 4, label: 'Strong', color: 'bg-green-500' },
    ];

    setStrength(strengths[score]);
  }, [password]);

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-gray-400">Password Strength</span>
        <span className={`text-xs font-medium ${strength.color.replace('bg-', 'text-')}`}>
          {strength.label}
        </span>
      </div>
      
      <div className="h-1.5 w-full bg-gray-700 rounded-full overflow-hidden">
        {/* Colored progress bar */}
        <div 
          className={`h-full ${strength.color} transition-all duration-300 ease-out`}
          style={{ width: `${(strength.score / 4) * 100}%` }}
        ></div>
      </div>

      {/* Password requirements */}
      {password && (
        <ul className="mt-2 text-xs text-gray-400 space-y-1">
          <li className={password.length >= 8 ? 'text-green-400' : ''}>
            ✓ At least 8 characters
          </li>
          <li className={/[A-Z]/.test(password) ? 'text-green-400' : ''}>
            ✓ At least 1 uppercase letter
          </li>
          <li className={/[a-z]/.test(password) ? 'text-green-400' : ''}>
            ✓ At least 1 lowercase letter
          </li>
          <li className={/[0-9]/.test(password) ? 'text-green-400' : ''}>
            ✓ At least 1 number
          </li>
          <li className={/[^A-Za-z0-9]/.test(password) ? 'text-green-400' : ''}>
            ✓ At least 1 special character
          </li>
        </ul>
      )}
    </div>
  );
};

export default PasswordStrength; 