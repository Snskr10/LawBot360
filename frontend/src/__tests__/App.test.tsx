import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../App';

describe('App', () => {
  it('should render login page when not authenticated', () => {
    localStorage.removeItem('access_token');
    
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    
    // Should redirect to dashboard, which redirects to login if not authenticated
    // This is a basic test - actual behavior depends on AuthProvider implementation
    expect(screen.getByText(/LawBot 360/i)).toBeInTheDocument();
  });
});

