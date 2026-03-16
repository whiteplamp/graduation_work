import api from './apiClient';

export const supplierService = {
  async getList() {
    const { data } = await api.get('/suppliers');
    return data;
  },

  async create(payload) {
    const { data } = await api.post('/suppliers', payload);
    return data;
  },

  async update(id, payload) {
    const { data } = await api.put(`/suppliers/${id}`, payload);
    return data;
  },

  async remove(id) {
    await api.delete(`/suppliers/${id}`);
  },
};

