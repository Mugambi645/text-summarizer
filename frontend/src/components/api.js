import axios from "axios";

let accessToken = null;
export function setAccessToken(token) { accessToken = token; }
export function getAccessToken() { return accessToken; }

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true, // sends cookies (for refresh)
});

// attach access token
api.interceptors.request.use(config => {
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
  return config;
});

// response interceptor to handle 401 and refresh
api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config;
    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      // call refresh endpoint, cookie is auto-sent
      try {
        const refreshRes = await axios.post(
          "http://localhost:8000/api/auth/refresh/",
          {},
          { withCredentials: true }
        );
        // update access token in memory
        accessToken = refreshRes.data.access;
        // retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return axios(originalRequest);
      } catch (refreshErr) {
        // redirect to login or clear state
        return Promise.reject(refreshErr);
      }
    }
    return Promise.reject(err);
  }
);

export default api;
