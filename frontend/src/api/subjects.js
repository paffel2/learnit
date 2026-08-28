import apiClient from './client';

// API методы - без интерфейсов
export const subjectsAPI = {
  /**
   * Получить список всех предметов
   * @param {number} page - Номер страницы (по умолчанию 1)
   * @returns {Promise<Array>}
   */
  list: async (page = 1) => {
    const response = await apiClient.get('/api/v1/subjects/', {
      params: { page }
    });
    return response.data;
  },

  /**
   * Получить один предмет
   * @param {number} subjectId - ID предмета
   * @returns {Promise<Object>}
   */
  get: async (subjectId) => {
    const response = await apiClient.get(`/api/v1/subjects/${subjectId}`);
    return response.data;
  },

  /**
   * Создать новый предмет
   * @param {Object} data - Данные для создания
   * @param {string} data.name - Название предмета
   * @returns {Promise<Object>}
   */
  create: async (data) => {
    const response = await apiClient.post('/api/v1/subjects/', data);
    return response.data;
  },

  /**
   * Обновить предмет
   * @param {number} subjectId - ID предмета
   * @param {Object} data - Данные для обновления
   * @param {string} data.name - Название предмета
   * @param {number} data.order - Порядок
   * @returns {Promise<Object>}
   */
  update: async (subjectId, data) => {
    const response = await apiClient.put(`/api/v1/subjects/${subjectId}`, data);
    return response.data;
  },

  /**
   * Частично обновить предмет
   * @param {number} subjectId - ID предмета
   * @param {Object} data - Данные для частичного обновления
   * @param {string} [data.name] - Название предмета
   * @param {number} [data.order] - Порядок
   * @returns {Promise<Object>}
   */
  patch: async (subjectId, data) => {
    const response = await apiClient.patch(`/api/v1/subjects/${subjectId}`, data);
    return response.data;
  },

  /**
   * Удалить предмет
   * @param {number} subjectId - ID предмета
   * @returns {Promise<void>}
   */
  delete: async (subjectId) => {
    await apiClient.delete(`/api/v1/subjects/${subjectId}`);
  },
};