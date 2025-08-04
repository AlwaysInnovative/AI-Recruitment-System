// src/services/api.js
const API_BASE = 'https://ai-recruitment-system.onrender.com';

export const api = {
  // Candidate endpoints
  getCandidates: async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE}/candidates?${query}`);
    return response.json();
  },

  createCandidate: async (candidateData) => {
    const response = await fetch(`${API_BASE}/candidates`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(candidateData),
    });
    return response.json();
  },

  // Job endpoints
  getJobs: async () => {
    const response = await fetch(`${API_BASE}/jobs`);
    return response.json();
  },

  // Analytics endpoints
  getDashboardStats: async () => {
    const response = await fetch(`${API_BASE}/analytics/dashboard`);
    return response.json();
  }
};
