import { useState, useEffect } from 'react';
import { getMe } from '../api/authService';

function MyInfo() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchMyData = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await getMe();
        setUserData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMyData();
  }, []); // 空依賴陣列，表示只在元件初次渲染時執行一次

  if (loading) {
    return <p>正在載入你的資訊...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>載入失敗：{error}</p>;
  }

  if (!userData) {
    return <p>找不到使用者資料。</p>;
  }

  return (
    <div style={{ textAlign: 'left', maxWidth: '400px', margin: '0 auto' }}>
      <h3>你的個人檔案</h3>
      <p><strong>ID:</strong> {userData.id}</p>
      <p><strong>帳號:</strong> {userData.username}</p>
      <p><strong>全名:</strong> {userData.full_name || '未提供'}</p>
      <p><strong>Email:</strong> {userData.email || '未提供'}</p>
      <p><strong>電話:</strong> {userData.phone || '未提供'}</p>
      <p><strong>性別:</strong> {userData.gender || '未提供'}</p>
      <p><strong>生日:</strong> {userData.birthday ? new Date(userData.birthday).toLocaleDateString() : '未提供'}</p>
      <p><strong>角色:</strong> {userData.role}</p>
    </div>
  );
}

export default MyInfo;
