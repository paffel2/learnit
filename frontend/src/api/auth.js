import apiClient from './client';

export const authAPI = {
  // Регистрация
  register: async (data) => {
    const response = await apiClient.post('/api/v1/users/registration', data);
    return response.data;
  },

  // Вход
  login: async (data) => {
    const response = await apiClient.post('/api/v1/users/login', data);
    // Предполагаем, что токен приходит в ответе
    if (response.data.token) {
      localStorage.setItem('access_token', response.data.token);
    }
    return response.data;
  },

  // Обновление токена
  refresh: async () => {
    const response = await apiClient.get('/api/v1/users/refresh', {
      withCredentials: true,
    });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    return response.data;
  },

  // Выход
  logout: () => {
    localStorage.removeItem('access_token');
  },
};