import api from './apiClient';

export const statisticsService = {
  async getAnalytics(params) {
    const { data } = await api.get('/statistics/analytics', { params });
    return data;
  },

  async exportReport(params) {
    const { data, headers } = await api.get('/statistics/export', {
      params,
      responseType: 'blob',
    });

    const disposition = headers['content-disposition'] || '';
    const match = disposition.match(/filename="?(.+)"?/i);
    const filename = match ? match[1] : 'analytics.xlsx';

    const url = window.URL.createObjectURL(data);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};

