// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://stgi-calculatorpro.koyeb.app/api', 
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const initCSRF = async () => {
  try {
    await api.get('/auth/csrf/');
    console.log('CSRF token initialized');
  } catch (error) {
    console.error('CSRF initialization failed:', error);
  }
};

// Intercept requests to add CSRF token
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }

  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data);
    
    if (error.response?.status === 401) {
      window.location.href = '/login?session_expired=true';
    }
    return Promise.reject(error);
  }
);

export default api;