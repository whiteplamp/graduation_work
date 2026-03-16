import api from './apiClient';

export const uploadService = {
  async uploadFile(file, mode) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);

    const { data } = await api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    return data;
  },

  async getStatus(jobId) {
    const { data } = await api.get(`/upload/${jobId}/status`);
    return data;
  },

  async startProcessing(jobId, payload) {
    await api.post(`/upload/${jobId}/process`, payload);
  },

  async downloadErrorReport(jobId) {
    const { data, headers } = await api.get(`/upload/${jobId}/errors`, {
      responseType: 'blob',
    });

    const disposition = headers['content-disposition'] || '';
    const match = disposition.match(/filename="?(.+)"?/i);
    const filename = match ? match[1] : 'errors.xlsx';

    const url = window.URL.createObjectURL(data);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  async getRecentJobs() {
    const { data } = await api.get('/upload/jobs/recent');
    return data;
  },
};

