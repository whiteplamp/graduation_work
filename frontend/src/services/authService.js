import api from './apiClient';

export const authService = {
  async login(payload) {
    const { data } = await api.post('/auth/login', payload);
    return {
      token: data.token,
      user: data.user,
    };
  },

  async register(payload) {
    const { data } = await api.post('/auth/register', payload);
    return {
      token: data.token,
      user: data.user,
    };
  },

  async logout() {
    await api.post('/auth/logout');
  },
};

