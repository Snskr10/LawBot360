import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60_000, // Increased timeout for OpenAI API calls
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    // Allow chat/explain endpoints without auth
    if (token && !config.url?.includes('/api/explain') && !config.url?.includes('/api/chat')) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Chat API function - ChatGPT-like interface
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  message: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export const sendChatMessage = async (messages: ChatMessage[], userMessage: string): Promise<ChatResponse> => {
  const response = await apiClient.post('/api/chat/', {
    messages,
    message: userMessage,
  });
  return response.data;
};

// Auth interfaces
export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  role?: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

// Auth API functions
export const login = async (payload: LoginPayload): Promise<AuthResponse> => {
  const response = await apiClient.post('/api/auth/login', payload);
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
  }
  return response.data;
};

export const register = async (payload: RegisterPayload): Promise<AuthResponse> => {
  const response = await apiClient.post('/api/auth/register', payload);
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
  }
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get('/api/auth/me');
  return response.data;
};

export const logout = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
};

export const getStoredUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('access_token');
};

// Contract API functions
export interface GenerateContractPayload {
  contract_type: string;
  parties: string[];
  terms: Record<string, unknown>;
  jurisdiction: string;
  language: string;
}

export const generateContract = async (payload: GenerateContractPayload) => {
  const response = await apiClient.post('/api/contracts/generate', payload);
  return response.data;
};

export const verifyDocument = async (formData: FormData) => {
  const response = await apiClient.post('/api/verify/document', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const explainClause = async (payload: { text: string; jurisdiction: string; language: string }) => {
  const response = await apiClient.post('/api/explain/', payload);
  return response.data;
};

export const fetchDashboardMetrics = async () => {
  const response = await apiClient.get('/api/dashboard/metrics');
  return response.data;
};
