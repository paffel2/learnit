import apiClient from './client';

export const questionsAPI = {
  // Получить все вопросы темы
  list: async (subjectId, themeId) => {
    const response = await apiClient.get(
      `/api/v1/questions/${subjectId}/themes/${themeId}/questions`
    );
    return response.data;
  },

  // Получить один вопрос
  get: async (subjectId, themeId, questionId) => {
    const response = await apiClient.get(
      `/api/v1/questions/${subjectId}/themes/${themeId}/questions/${questionId}`
    );
    return response.data;
  },

  // Создать вопрос
  create: async (subjectId, themeId, data) => {
    const response = await apiClient.post(
      `/api/v1/questions/${subjectId}/themes/${themeId}/questions`,
      data
    );
    return response.data;
  },

  // Обновить вопрос
  update: async (subjectId, themeId, questionId, data) => {
    const response = await apiClient.put(
      `/api/v1/questions/${subjectId}/themes/${themeId}/questions/${questionId}`,
      data
    );
    return response.data;
  },

  // Удалить вопрос
  delete: async (subjectId, themeId, questionId) => {
    await apiClient.delete(
      `/api/v1/questions/${subjectId}/themes/${themeId}/questions/${questionId}`
    );
  },
};