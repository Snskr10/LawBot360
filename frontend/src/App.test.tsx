import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders dashboard within layout shell', () => {
  render(
    <MemoryRouter initialEntries={['/dashboard']}>
      <App />
    </MemoryRouter>
  );

  expect(screen.getByRole('link', { name: /LawBot 360/i })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: /dashboard/i })).toBeInTheDocument();
});
