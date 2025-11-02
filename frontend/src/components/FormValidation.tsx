import React, { useState, useRef, useEffect } from 'react';
import './FormValidation.css';

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: string, allValues?: Record<string, string>) => string | null;
  message?: string;
}

export interface FieldValidation {
  [key: string]: ValidationRule;
}

interface UseFormValidationProps {
  fields: FieldValidation;
  onSubmit: (data: Record<string, string>) => void | Promise<void>;
}

export function useFormValidation({ fields, onSubmit }: UseFormValidationProps) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = (name: string, value: string): string | null => {
    const rule = fields[name];
    if (!rule) return null;

    if (rule.required && !value.trim()) {
      return rule.message || `${name} is required`;
    }

    if (value.trim() && rule.minLength && value.length < rule.minLength) {
      return rule.message || `${name} must be at least ${rule.minLength} characters`;
    }

    if (value.trim() && rule.maxLength && value.length > rule.maxLength) {
      return rule.message || `${name} must be no more than ${rule.maxLength} characters`;
    }

    if (value.trim() && rule.pattern && !rule.pattern.test(value)) {
      return rule.message || `${name} format is invalid`;
    }

    if (value.trim() && rule.custom) {
      return rule.custom(value, values);
    }

    return null;
  };

  const validateAll = (): boolean => {
    const newErrors: Record<string, string> = {};
    let isValid = true;

    Object.keys(fields).forEach((name) => {
      const error = validateField(name, values[name] || '');
      if (error) {
        newErrors[name] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (name: string, value: string) => {
    setValues((prev) => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleBlur = (name: string) => {
    setTouched((prev) => ({ ...prev, [name]: true }));
    const error = validateField(name, values[name] || '');
    if (error) {
      setErrors((prev) => ({ ...prev, [name]: error }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched: Record<string, boolean> = {};
    Object.keys(fields).forEach((name) => {
      allTouched[name] = true;
    });
    setTouched(allTouched);

    if (validateAll()) {
      await onSubmit(values);
    }
  };

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    handleSubmit,
    setValues,
    setErrors,
  };
}

interface ValidatedInputProps {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
  value: string;
  error?: string;
  touched?: boolean;
  onChange: (value: string) => void;
  onBlur: () => void;
  required?: boolean;
  disabled?: boolean;
}

export function ValidatedInput({
  name,
  label,
  type = 'text',
  placeholder,
  value,
  error,
  touched,
  onChange,
  onBlur,
  required,
  disabled,
}: ValidatedInputProps) {
  const showError = touched && error;

  return (
    <div className={`form-field ${showError ? 'has-error' : ''}`}>
      <label htmlFor={name}>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
        placeholder={placeholder}
        disabled={disabled}
        className={showError ? 'error' : ''}
        aria-invalid={showError ? true : false}
        aria-describedby={showError ? `${name}-error` : undefined}
      />
      {showError && (
        <span id={`${name}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
    </div>
  );
}

interface ValidatedTextareaProps {
  name: string;
  label: string;
  placeholder?: string;
  value: string;
  error?: string;
  touched?: boolean;
  onChange: (value: string) => void;
  onBlur: () => void;
  required?: boolean;
  disabled?: boolean;
  rows?: number;
}

export function ValidatedTextarea({
  name,
  label,
  placeholder,
  value,
  error,
  touched,
  onChange,
  onBlur,
  required,
  disabled,
  rows = 4,
}: ValidatedTextareaProps) {
  const showError = touched && error;

  return (
    <div className={`form-field ${showError ? 'has-error' : ''}`}>
      <label htmlFor={name}>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
        placeholder={placeholder}
        disabled={disabled}
        rows={rows}
        className={showError ? 'error' : ''}
        aria-invalid={showError ? true : false}
        aria-describedby={showError ? `${name}-error` : undefined}
      />
      {showError && (
        <span id={`${name}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
    </div>
  );
}

interface ValidatedSelectProps {
  name: string;
  label: string;
  value: string;
  error?: string;
  touched?: boolean;
  onChange: (value: string) => void;
  onBlur: () => void;
  required?: boolean;
  disabled?: boolean;
  options: Array<{ value: string; label: string }>;
}

export function ValidatedSelect({
  name,
  label,
  value,
  error,
  touched,
  onChange,
  onBlur,
  required,
  disabled,
  options,
}: ValidatedSelectProps) {
  const showError = touched && error;

  return (
    <div className={`form-field ${showError ? 'has-error' : ''}`}>
      <label htmlFor={name}>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <select
        id={name}
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
        disabled={disabled}
        className={showError ? 'error' : ''}
        aria-invalid={showError ? true : false}
        aria-describedby={showError ? `${name}-error` : undefined}
      >
        {!required && <option value="">Select...</option>}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {showError && (
        <span id={`${name}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
    </div>
  );
}

