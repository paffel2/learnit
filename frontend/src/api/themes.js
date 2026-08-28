import apiClient from './client';

export const themesAPI = {
  // Получить все темы предмета
  list: async (subjectId) => {
    const response = await apiClient.get(`/api/v1/subjects/${subjectId}/themes`);
    return response.data;
  },

  // Получить одну тему
  get: async (subjectId, themeId) => {
    const response = await apiClient.get(`/api/v1/subjects/${subjectId}/themes/${themeId}`);
    return response.data;
  },

  // Создать тему
  create: async (subjectId, data) => {
    const response = await apiClient.post(`/api/v1/subjects/${subjectId}/themes`, data);
    return response.data;
  },

  // Обновить тему
  update: async (subjectId, themeId, data) => {
    const response = await apiClient.put(`/api/v1/subjects/${subjectId}/themes/${themeId}`, data);
    return response.data;
  },

  // Удалить тему
  delete: async (subjectId, themeId) => {
    await apiClient.delete(`/api/v1/subjects/${subjectId}/themes/${themeId}`);
  },
};