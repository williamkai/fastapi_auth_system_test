import { useState, useEffect } from 'react';
import { getUsers, updateUserStatus, deleteUser } from '../api/authService';
import { useAuth } from '../context/AuthContext';

// --- 詳細資訊彈出視窗元件 ---
function UserDetailModal({ user, onClose }) {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('zh-TW', { hour12: false });
  };

  return (
    <div style={styles.modalOverlay}>
      <div style={styles.modalContent}>
        <h3>使用者詳細資訊: {user.username}</h3>
        <div style={styles.modalBody}>
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>全名:</strong> {user.full_name || '未提供'}</p>
          <p><strong>Email:</strong> {user.email || '未提供'}</p>
          <p><strong>電話:</strong> {user.phone || '未提供'}</p>
          <p><strong>性別:</strong> {user.gender || '未提供'}</p>
          <p><strong>生日:</strong> {user.birthday ? new Date(user.birthday).toLocaleDateString() : '未提供'}</p>
          <p><strong>角色:</strong> {user.role}</p>
          <p><strong>狀態:</strong> {user.is_active ? '啟用' : '停用'}</p>
          <p><strong>建立時間:</strong> {formatDate(user.created_at)}</p>
          <p><strong>最後更新:</strong> {formatDate(user.updated_at)}</p>
          <p><strong>最後登入:</strong> {formatDate(user.last_login)}</p>
        </div>
        <button onClick={onClose} style={styles.closeButton}>關閉</button>
      </div>
    </div>
  );
}


function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedUser, setSelectedUser] = useState(null); // 用來控制彈出視窗
  const { user: currentUser } = useAuth();

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getUsers();
      setUsers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleToggleStatus = async (user) => {
    if (!window.confirm(`你確定要將使用者 ${user.username} 的狀態切換為 ${user.is_active ? '停用' : '啟用'} 嗎？`)) {
      return;
    }
    try {
      await updateUserStatus(user.id, !user.is_active);
      await fetchUsers();
    } catch (err) {
      alert(`操作失敗：${err.message}`);
    }
  };

  const handleDeleteUser = async (user) => {
    if (!window.confirm(`你確定要永久刪除使用者 ${user.username} 嗎？此操作無法復原。`)) {
      return;
    }
    try {
      await deleteUser(user.id);
      await fetchUsers();
    } catch (err) {
      alert(`刪除失敗：${err.message}`);
    }
  };

  if (loading) return <p>正在載入使用者列表...</p>;
  if (error) return <p style={{ color: 'red' }}>載入失敗：{error}</p>;

  return (
    <div style={{ width: '100%' }}>
      <h3>使用者管理</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #4a6fa5' }}>
            <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>帳號</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>角色</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>狀態</th>
            <th style={{ padding: '8px', textAlign: 'center' }}>操作</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id} style={{ borderBottom: '1px solid #555' }}>
              <td style={{ padding: '8px' }}>{user.id}</td>
              <td style={{ padding: '8px' }}>{user.username}</td>
              <td style={{ padding: '8px' }}>{user.role}</td>
              <td style={{ padding: '8px' }}>
                <span style={{ color: user.is_active ? 'lightgreen' : 'salmon' }}>
                  {user.is_active ? '啟用' : '停用'}
                </span>
              </td>
              <td style={{ padding: '8px', textAlign: 'center' }}>
                <button onClick={() => setSelectedUser(user)} style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem', marginRight: '5px', backgroundColor: '#17a2b8' }}>
                  詳細資訊
                </button>
                {currentUser?.username !== user.username && user.role !== 'admin' && (
                  <>
                    <button onClick={() => handleToggleStatus(user)} style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem', marginRight: '5px' }}>
                      切換狀態
                    </button>
                    <button onClick={() => handleDeleteUser(user)} style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem', backgroundColor: '#dc3545' }}>
                      刪除
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* 如果 selectedUser 有值，就顯示彈出視窗 */}
      {selectedUser && <UserDetailModal user={selectedUser} onClose={() => setSelectedUser(null)} />}
    </div>
  );
}

// --- 內聯樣式，方便管理 ---
const styles = {
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  modalContent: {
    backgroundColor: '#2e313c',
    padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)',
    width: '90%',
    maxWidth: '500px',
    color: '#ffffff',
    borderTop: '2px solid #4a6fa5',
  },
  modalBody: {
    textAlign: 'left',
    maxHeight: '60vh',
    overflowY: 'auto',
    paddingRight: '10px',
  },
  closeButton: {
    marginTop: '20px',
    padding: '0.6rem 1.2rem',
    backgroundColor: '#6c757d',
  }
};

export default UserManagement;
