import api from './apiClient';

export const productService = {
  async getList(params) {
    const { data } = await api.get('/products', { params });
    return data;
  },

  async create(payload) {
    const { data } = await api.post('/products', payload);
    return data;
  },

  async update(id, payload) {
    const { data } = await api.put(`/products/${id}`, payload);
    return data;
  },

  async remove(id) {
    await api.delete(`/products/${id}`);
  },
};

