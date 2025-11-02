import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { login, register, logout, isAuthenticated, getStoredUser } from '../api/client';

// Mock the API client
jest.mock('../api/client');

const TestComponent = () => {
  const { user, isAuthenticated: authIsAuthenticated, login: authLogin, logout: authLogout } = useAuth();
  
  return (
    <div>
      <div data-testid="user">{user ? user.name : 'No user'}</div>
      <div data-testid="authenticated">{authIsAuthenticated ? 'Yes' : 'No'}</div>
      <button onClick={() => authLogin('test@example.com', 'password')}>Login</button>
      <button onClick={() => authLogout()}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  it('should provide auth context', () => {
    (getStoredUser as jest.Mock).mockReturnValue(null);
    (isAuthenticated as jest.Mock).mockReturnValue(false);
    
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    expect(screen.getByTestId('user')).toHaveTextContent('No user');
    expect(screen.getByTestId('authenticated')).toHaveTextContent('No');
  });

  it('should handle login', async () => {
    (getStoredUser as jest.Mock).mockReturnValue(null);
    (isAuthenticated as jest.Mock).mockReturnValue(false);
    (login as jest.Mock).mockResolvedValue({
      user: { id: 1, name: 'Test User', email: 'test@example.com', role: 'user' },
      access_token: 'token123'
    });
    
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    const loginButton = screen.getByText('Login');
    loginButton.click();
    
    await waitFor(() => {
      expect(login).toHaveBeenCalledWith('test@example.com', 'password');
    });
  });
});

describe('API Client', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should check authentication status', () => {
    localStorage.setItem('access_token', 'test-token');
    expect(isAuthenticated()).toBe(true);
    
    localStorage.removeItem('access_token');
    expect(isAuthenticated()).toBe(false);
  });
});

