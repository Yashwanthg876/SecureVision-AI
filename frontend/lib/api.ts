import axios from 'axios';

const api = axios.create({
  baseURL: typeof window !== 'undefined' ? '/api/v1' : 'http://localhost:8000/api/v1',
  withCredentials: true, // important for cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response?.status === 401 &&
      typeof window !== 'undefined' &&
      !window.location.pathname.startsWith('/login')
    ) {
      const next = `${window.location.pathname}${window.location.search}`;
      window.location.replace(`/login?next=${encodeURIComponent(next)}`);
    }
    return Promise.reject(error);
  },
);

export default api;
