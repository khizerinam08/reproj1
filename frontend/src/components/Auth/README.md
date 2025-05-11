# Authentication Components

This directory contains the components for authentication functionality.

## Components

### `FormInput.js`
A reusable form input component with validation support. It's designed to work with React Hook Form and displays validation errors.

```jsx
<FormInput
  id="email"
  name="email"
  label="Email Address"
  type="email"
  placeholder="Enter your email address"
  register={register}
  errors={errors}
  required
/>
```

### `PasswordStrength.js`
Password strength indicator that visually shows the strength of a password based on length, character variety, etc.

```jsx
<PasswordStrength password={watchPassword} />
```

### `SignUpForm.js`
Main form component for user registration. Includes validation, API integration, and error handling.

```jsx
<SignUpForm />
```

### `LoginForm.js`
Form component for user login. Handles form validation, submission, and redirects after successful login.

```jsx
<LoginForm />
```

### `ForgotPasswordForm.js`
Form for requesting a password reset. Sends a reset link to the user's email.

```jsx
<ForgotPasswordForm />
```

### `ResetPasswordForm.js`
Form for setting a new password after receiving a reset token. Includes password strength validation.

```jsx
<ResetPasswordForm token={resetToken} />
```

### `ProtectedRoute.js`
Route wrapper that restricts access to authenticated users only. Redirects to login page if not authenticated.

```jsx
<Route 
  path="/secure-page" 
  element={
    <ProtectedRoute>
      <SecurePage />
    </ProtectedRoute>
  } 
/>
```

### Development/Testing Tools

#### `SignUpApiTest.js`
A development tool to test API connectivity for registration endpoints.

#### `LoginApiTest.js`
A development tool to test API connectivity for login endpoints.

#### `PasswordResetApiTest.js`
A development tool to test API connectivity for password reset endpoints.

## Usage

### Form Validation
The forms use Yup and React Hook Form for validation. The validation schemas ensure:

- Name is between 2-50 characters
- Email is valid
- Password meets complexity requirements
- Passwords match when confirming

### API Integration
The forms connect to the backend API through the `authService` and the `AuthContext`.

### Error Handling
- Form validation errors are displayed below each input
- API errors are displayed at the top of the form
- Loading states are managed to disable the form during submission

## Best Practices

- All inputs have proper accessibility attributes
- Password fields include strength indicators
- Errors are clearly communicated to users
- Loading states prevent multiple submissions
- Form retains values on validation errors 