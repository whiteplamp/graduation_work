import api from './apiClient';

export const settingsService = {
  async getImportSettings() {
    const { data } = await api.get('/settings/import');
    return data;
  },

  async updateImportSettings(payload) {
    const { data } = await api.put('/settings/import', payload);
    return data;
  },
};

