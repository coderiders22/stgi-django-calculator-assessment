// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',  
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const initCSRF = async () => {
  try {
    await api.get('/auth/csrf/', { withCredentials: true });
  
  } catch (error) {
  
  }
};


api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }

  
  config.withCredentials = true;



  return config;
});


api.interceptors.response.use(
  (response) => {
   
    return response;
  },
  (error) => {
  
    
    if (error.response?.status === 401) {
    
      window.location.href = '/login?session_expired=true';
    }
    return Promise.reject(error);
  }
);

export default api;