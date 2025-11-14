import { refreshToken } from './authService';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8010';
// 'http://127.0.0.1:8010','https://fastapi-auth-system-test.onrender.com'

// A flag to prevent multiple concurrent refresh attempts
let isRefreshing = false;
// A queue to hold requests that failed while the token was being refreshed
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const handleLogout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  window.location.reload(); // 強制重整頁面，AuthContext 會自動處理後續
};

/**
 * 一個封裝了 fetch 的函數，會自動加入 Authorization header，並處理 token refresh。
 * @param {string} endpoint - API 的端點，例如 '/me'
 * @param {object} options - fetch 的設定物件，例如 method, body 等
 */
export async function apiFetch(endpoint, options = {}) {
  let token = localStorage.getItem('accessToken');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

  if (response.status === 401) {
    if (!isRefreshing) {
      isRefreshing = true;
      try {
        const newTokens = await refreshToken();
        localStorage.setItem('accessToken', newTokens.access_token);
        localStorage.setItem('refreshToken', newTokens.refresh_token);

        processQueue(null, newTokens.access_token);

        // 重試原始請求
        headers['Authorization'] = `Bearer ${newTokens.access_token}`;
        response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

      } catch (error) {
        processQueue(error, null);
        handleLogout(); // Refresh token 也過期了，登出使用者
        return Promise.reject(error);
      } finally {
        isRefreshing = false;
      }
    } else {
      // 如果正在刷新 token，將失敗的請求加入隊列
      return new Promise((resolve, reject) => {
        failedQueue.push({
          resolve: (newToken) => {
            headers['Authorization'] = `Bearer ${newToken}`;
            resolve(fetch(`${API_URL}${endpoint}`, { ...options, headers }));
          },
          reject,
        });
      });
    }
  }

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `API 請求失敗，狀態碼: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
