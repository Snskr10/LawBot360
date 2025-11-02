import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
  fullScreen?: boolean;
}

export default function LoadingSpinner({ 
  size = 'medium', 
  message, 
  fullScreen = false 
}: LoadingSpinnerProps) {
  const content = (
    <div className={`loading-spinner-container ${fullScreen ? 'fullscreen' : ''}`}>
      <div className={`spinner spinner-${size}`}>
        <div className="spinner-circle"></div>
      </div>
      {message && <p className="loading-message">{message}</p>}
    </div>
  );

  return content;
}

interface LoadingButtonProps {
  loading: boolean;
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

export function LoadingButton({ loading, children, className = '', disabled }: LoadingButtonProps) {
  return (
    <button className={`loading-button ${className}`} disabled={loading || disabled}>
      {loading && <span className="button-spinner"></span>}
      <span className={loading ? 'button-text-loading' : ''}>{children}</span>
    </button>
  );
}

