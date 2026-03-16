import api from './apiClient';

export const dashboardService = {
  async getOverview() {
    const { data } = await api.get('/dashboard/overview');
    return data;
  },
};

