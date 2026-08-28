import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Важно для работы с cookie
});

// Интерцептор для добавления токена
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Authorization header set:', config.headers.Authorization); // Для отладки
    }
    console.log('Authorization header set:', config.headers.Authorization); // Для отладки
    return config;
  },
  (error) => Promise.reject(error)
);

// Интерцептор для обновления токена
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Пытаемся обновить токен
        const response = await apiClient.get('/api/v1/users/refresh', {
          withCredentials: true,
        });
        
        // Предполагаем, что токен приходит в заголовке или теле ответа
        const newToken = response.data.access_token || response.headers.authorization?.split(' ')[1];
        
        if (newToken) {
          localStorage.setItem('access_token', newToken);
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Если обновить не удалось - выходим
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;