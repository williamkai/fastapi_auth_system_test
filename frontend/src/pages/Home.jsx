import { useState } from "react";
import { Link } from "react-router-dom";
import MyInfo from "../components/MyInfo";
import UserManagement from "../components/UserManagement"; // 引入 UserManagement 元件
import { useAuth } from "../context/AuthContext";

// --- 未登入時顯示的公開頁面 ---
function PublicHome() {
  return (
    <>
      {/* <div className="separator"></div> */}
      <section>
        <p>歡迎來到 FastAPI 用戶管理系統測試。</p>
        <p>請登入以繼續，或註冊新帳戶。</p>
        <h2>請選擇操作</h2>
        <div className="card">
          <Link to="/login">
            <button>登入</button>
          </Link>
          <Link to="/register">
            <button>註冊</button>
          </Link>
        </div>
      </section>
    </>
  );
}

// --- 登入後顯示的控制台頁面 ---
function Dashboard() {
  const { user, logout } = useAuth();
  const [view, setView] = useState('main'); // 'main', 'myInfo', 'userManagement'

  const renderMainView = () => (
    <>
      <h2>控制台</h2>
      <p>歡迎回來, <strong>{user?.username}</strong>! 你的角色是: <strong>{user?.role}</strong>.</p>
      <div className="card" style={{ flexDirection: 'row', justifyContent: 'center', gap: '1rem' }}>
        <button onClick={() => setView('myInfo')}>我的資訊</button>

        {user?.role === 'admin' && (
          <button onClick={() => setView('userManagement')} style={{ backgroundColor: '#dc3545' }}>使用者管理</button>
        )}

        <button onClick={logout} style={{ backgroundColor: '#6c757d' }}>登出</button>
      </div>
    </>
  );

  const renderCurrentView = () => {
    switch (view) {
      case 'myInfo':
        return <MyInfo />;
      case 'userManagement':
        return <UserManagement />;
      default:
        return renderMainView();
    }
  };

  return (
    <section>
      {view !== 'main' && (
        <button onClick={() => setView('main')} style={{ marginBottom: '1rem' }}>
          &larr; 返回控制台
        </button>
      )}
      {renderCurrentView()}
    </section>
  );
}


// --- Home 元件現在是調度中心 ---
function Home() {
  const { user } = useAuth(); // 從 context 取得 user 狀態

  return user ? <Dashboard /> : <PublicHome />;
}

export default Home;
