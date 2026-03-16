import api from './apiClient';

export const profileService = {
  async getProfile() {
    const { data } = await api.get('/profile');
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.put('/profile', payload);
    return data;
  },

  async changePassword(payload) {
    await api.post('/profile/change-password', payload);
  },
};

