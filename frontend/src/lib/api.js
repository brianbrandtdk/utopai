// API configuration with environment variable support
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://utopai-production.up.railway.app';

// API client with error handling
class ApiClient {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api`;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      credentials: 'include', // Include cookies for session management
      ...options,
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: userData,
    });
  }

  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: credentials,
    });
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async selectTheme(theme) {
    return this.request('/auth/select-theme', {
      method: 'POST',
      body: { theme },
    });
  }

  // Islands endpoints
  async getIslands() {
    return this.request('/islands');
  }

  async getIslandActivities(islandId) {
    return this.request(`/islands/${islandId}/activities`);
  }

  async startActivity(activityId) {
    return this.request(`/activities/${activityId}/start`, {
      method: 'POST',
    });
  }

  async completeActivity(activityId, score = 0) {
    return this.request(`/activities/${activityId}/complete`, {
      method: 'POST',
      body: { score },
    });
  }
}

export const api = new ApiClient();

