import { createContext, useState, useEffect, useContext } from 'react';
import { jwtDecode } from 'jwt-decode'; // 我們需要一個套件來解碼 JWT

// 1. 建立 Context
const AuthContext = createContext(null);

// 2. 建立 Provider 元件
export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    // 當 accessToken 改變時，解碼它並設定 user 狀態
    if (accessToken) {
      try {
        const decoded = jwtDecode(accessToken); // 解碼 token
        setUser({ username: decoded.sub, role: decoded.role });
        localStorage.setItem('accessToken', accessToken);
      } catch (error) {
        console.error("Invalid token:", error);
        logout(); // 如果 token 無效，就登出
      }
    } else {
      localStorage.removeItem('accessToken');
    }
  }, [accessToken]);

  useEffect(() => {
    // 當 refreshToken 改變時，更新 localStorage
    if (refreshToken) {
      localStorage.setItem('refreshToken', refreshToken);
    } else {
      localStorage.removeItem('refreshToken');
    }
  }, [refreshToken]);

  const login = (newAccessToken, newRefreshToken) => {
    setAccessToken(newAccessToken);
    setRefreshToken(newRefreshToken);
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
  };

  const authValue = {
    accessToken,
    refreshToken,
    user,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={authValue}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. 建立一個 custom hook，方便其他元件使用 context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
