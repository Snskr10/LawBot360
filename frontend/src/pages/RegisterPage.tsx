import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';
import { useFormValidation, ValidatedInput } from '../components/FormValidation';
import PageHeader from '../shared/PageHeader';
import './LoginPage.css';

export default function RegisterPage() {
  const { register } = useAuth();
  const { success, error: showError } = useToast();
  const navigate = useNavigate();

  const { values, errors, touched, handleChange, handleBlur, handleSubmit } = useFormValidation({
    fields: {
      name: {
        required: true,
        minLength: 2,
        message: 'Name must be at least 2 characters',
      },
      email: {
        required: true,
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: 'Please enter a valid email address',
      },
      password: {
        required: true,
        minLength: 6,
        message: 'Password must be at least 6 characters',
      },
      confirmPassword: {
        required: true,
        custom: (value, allValues) => {
          if (value !== (allValues?.password || '')) {
            return 'Passwords do not match';
          }
          return null;
        },
      },
    },
    onSubmit: async (data) => {
      try {
        await register(data.name, data.email, data.password);
        success('Account created successfully! Redirecting...');
        setTimeout(() => navigate('/dashboard'), 1000);
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error ||
          err.message ||
          'Registration failed. Please try again.';
        showError(errorMessage);
      }
    },
  });

  return (
    <div className="login-page">
      <div className="login-container">
        <PageHeader title="Register" subtitle="Create your LawBot 360 account" />
        
        <form onSubmit={handleSubmit} className="login-form">
          <ValidatedInput
            name="name"
            label="Full Name"
            value={values.name || ''}
            error={errors.name}
            touched={touched.name}
            onChange={(value) => handleChange('name', value)}
            onBlur={() => handleBlur('name')}
            required
          />

          <ValidatedInput
            name="email"
            label="Email"
            type="email"
            value={values.email || ''}
            error={errors.email}
            touched={touched.email}
            onChange={(value) => handleChange('email', value)}
            onBlur={() => handleBlur('email')}
            required
          />

          <ValidatedInput
            name="password"
            label="Password"
            type="password"
            value={values.password || ''}
            error={errors.password}
            touched={touched.password}
            onChange={(value) => handleChange('password', value)}
            onBlur={() => handleBlur('password')}
            required
          />

          <ValidatedInput
            name="confirmPassword"
            label="Confirm Password"
            type="password"
            value={values.confirmPassword || ''}
            error={errors.confirmPassword}
            touched={touched.confirmPassword}
            onChange={(value) => handleChange('confirmPassword', value)}
            onBlur={() => handleBlur('confirmPassword')}
            required
          />

          <button type="submit" className="btn-primary">
            Register
          </button>

          <p className="register-link">
            Already have an account? <Link to="/login">Login here</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

