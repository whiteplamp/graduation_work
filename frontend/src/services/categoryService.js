import api from './apiClient';

export const categoryService = {
  async getTree() {
    const { data } = await api.get('/categories/tree');
    return data;
  },

  async getFlatList() {
    const { data } = await api.get('/categories/flat');
    return data;
  },

  async create(payload) {
    const { data } = await api.post('/categories', payload);
    return data;
  },

  async update(id, payload) {
    const { data } = await api.put(`/categories/${id}`, payload);
    return data;
  },

  async remove(id) {
    await api.delete(`/categories/${id}`);
  },
};

