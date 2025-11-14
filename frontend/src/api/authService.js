import { apiFetch } from './api';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8010';
// 'http://127.0.0.1:8010','https://fastapi-auth-system-test.onrender.com'

/**
 * 註冊新使用者
 * @param {object} userData - 來自前端元件的原始使用者資料
 */
export async function registerUser(userData) {
  // 建立一個要發送到後端的資料副本 (payload)
  const payload = { ...userData };

  // --- 資料清洗與格式化 ---

  // 1. 將選填欄位的空字串轉換為 null
  for (const key of ['full_name', 'email', 'phone', 'gender']) {
    if (payload[key] === '') {
      payload[key] = null;
    }
  }

  // 2. 處理生日的格式
  if (payload.birthday) {
    // 將 'YYYY-MM-DD' 轉換為完整的 ISO 格式字串 (UTC 時間)
    payload.birthday = new Date(payload.birthday).toISOString();
  } else {
    payload.birthday = null;
  }

  // --- 發送 API 請求 ---

  const response = await fetch(`${API_URL}/api/v1/auth/register`, { // 註冊的 API 端點是 /register
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload), // 發送清洗過的資料
  });

  if (!response.ok) {
    // 如果 API 回應不成功，嘗試解析錯誤訊息
    const errorData = await response.json();
    // FastAPI 的驗證錯誤通常在 errorData.detail
    throw new Error(errorData.detail || '註冊失敗，請檢查你的輸入。');
  }

  // 如果註冊成功，回傳後端給的資料 (通常是新建立的使用者資訊)
  return response.json();
}

/**
 * 使用者登入
 * @param {string} username - 帳號
 * @param {string} password - 密碼
 */
export async function loginUser(username, password) {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: params,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || '登入失敗，請檢查帳號或密碼。');
  }

  return response.json(); // 回傳 { access_token, refresh_token, token_type }
}

/**
 * 使用 refresh token 換發新的 token
 */
export async function refreshToken() {
  const currentRefreshToken = localStorage.getItem('refreshToken');
  if (!currentRefreshToken) {
    throw new Error('No refresh token found');
  }

  const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: currentRefreshToken }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to refresh token');
  }

  return response.json();
}


// ===============================================
// 以下是需要驗證的 API 請求
// ===============================================

/**
 * 獲取當前登入使用者的資訊
 */
export function getMe() {
  return apiFetch('/api/v1/me');
}

/**
 * (Admin) 獲取所有使用者列表
 */
export function getUsers() {
  return apiFetch('/api/v1/users');
}

/**
 * (Admin) 更新使用者狀態
 * @param {number} userId - 使用者 ID
 * @param {boolean} isActive - 是否啟用
 */
export function updateUserStatus(userId, isActive) {
  return apiFetch(`/api/v1/users/${userId}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ is_active: isActive }),
  });
}

/**
 * (Admin) 刪除使用者
 * @param {number} userId - 使用者 ID
 */
export function deleteUser(userId) {
  return apiFetch(`/api/v1/users/${userId}`, {
    method: 'DELETE',
  });
}
