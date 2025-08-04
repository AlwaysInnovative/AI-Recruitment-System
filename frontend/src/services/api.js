const API_BASE = 'https://ai-recruitment-system.onrender.com';

export const api = {
  // Existing endpoints
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

  getJobs: async () => {
    const response = await fetch(`${API_BASE}/jobs`);
    return response.json();
  },

  // NEW Overview endpoints
  getOverviewStats: async () => {
    const response = await fetch(`${API_BASE}/overview/stats`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  getRecentActivity: async () => {
    const response = await fetch(`${API_BASE}/overview/activity`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  // Enhanced with error handling
  getDashboardStats: async () => {
    try {
      const [stats, activity] = await Promise.all([
        fetch(`${API_BASE}/overview/stats`),
        fetch(`${API_BASE}/overview/activity`)
      ]);
      
      if (!stats.ok || !activity.ok) {
        throw new Error('Failed to fetch dashboard data');
      }
      
      return {
        stats: await stats.json(),
        activity: (await activity.json()).activities
      };
    } catch (error) {
      console.error('Dashboard API Error:', error);
      throw error;
    }
  }
};
