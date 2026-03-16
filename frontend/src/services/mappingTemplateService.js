import api from './apiClient';

export const mappingTemplateService = {
  async getList() {
    const { data } = await api.get('/mapping-templates');
    return data;
  },

  async create(payload) {
    const { data } = await api.post('/mapping-templates', payload);
    return data;
  },

  async remove(id) {
    await api.delete(`/mapping-templates/${id}`);
  },
};

