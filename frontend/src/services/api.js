const API_BASE = 'https://ai-recruitment-system.onrender.com';

// Helper function for API requests
const makeRequest = async (endpoint, method = 'GET', body = null) => {
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, config);
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

export const api = {
  // Candidate endpoints
  getCandidates: async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return makeRequest(`/candidates?${query}`);
  },

  createCandidate: async (candidateData) => {
    return makeRequest('/candidates', 'POST', candidateData);
  },

  // Job endpoints
  getJobs: async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return makeRequest(`/jobs?${query}`);
  },

  // Overview endpoints
  getOverviewStats: async () => {
    return makeRequest('/overview/stats');
  },

  getRecentActivity: async () => {
    const data = await makeRequest('/overview/activity');
    return data.activities || [];
  },

  // Enhanced dashboard endpoint
  getDashboardStats: async () => {
    try {
      const [stats, activity] = await Promise.all([
        makeRequest('/overview/stats'),
        makeRequest('/overview/activity')
      ]);
      
      return {
        stats,
        activity: activity.activities || []
      };
    } catch (error) {
      console.error('Dashboard API Error:', error);
      throw new Error(`Failed to load dashboard: ${error.message}`);
    }
  },

  // Add authentication header helper
  setAuthToken: (token) => {
    // This would be used to modify the makeRequest function
    // to include the Authorization header when needed
    makeRequest.defaults = {
      ...makeRequest.defaults,
      headers: {
        ...makeRequest.defaults?.headers,
        Authorization: `Bearer ${token}`
      }
    };
  }
};

// Optional: Add request interceptors for global handling
let requestInterceptors = [];
let responseInterceptors = [];

export const addRequestInterceptor = (interceptor) => {
  requestInterceptors.push(interceptor);
};

export const addResponseInterceptor = (interceptor) => {
  responseInterceptors.push(interceptor);
};

// Enhanced makeRequest with interceptors
const enhancedMakeRequest = async (...args) => {
  let request = { endpoint: args[0], config: args[1] || {} };
  
  // Run request interceptors
  for (const interceptor of requestInterceptors) {
    request = await interceptor(request);
  }

  const response = await makeRequest(request.endpoint, request.config.method, request.config.body);
  
  // Run response interceptors
  let processedResponse = response;
  for (const interceptor of responseInterceptors) {
    processedResponse = await interceptor(processedResponse);
  }

  return processedResponse;
};

// Replace original makeRequest if using interceptors
// makeRequest = enhancedMakeRequest;
