import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default {
  // Jobs
  getJobs() {
    return apiClient.get('/jobs');
  },
  getJob(id) {
    return apiClient.get(`/jobs/${id}`);
  },
  
  // Candidates
  getCandidates() {
    return apiClient.get('/candidates');
  },
  
  // Applications
  getApplications() {
    return apiClient.get('/applications');
  },
  
  // Auth
  login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },
  
  // AI Matching
  getMatchScores() {
    return apiClient.get('/ai/matches');
  }
};
