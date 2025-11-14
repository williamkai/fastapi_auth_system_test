import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { loginUser } from "../api/authService";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); // 用來顯示錯誤訊息的 state
  const navigate = useNavigate();
  const { login } = useAuth(); // 從 AuthContext 取得 login 函數

  const handleLogin = async () => {
    setError(""); // 重設錯誤訊息
    if (!username || !password) {
      setError("請輸入帳號和密碼。");
      return;
    }

    try {
      const data = await loginUser(username, password);
      // 呼叫 context 的 login 函數，傳入 token
      login(data.access_token, data.refresh_token);
      // 導向到首頁
      navigate("/");
    } catch (err) {
      setError(err.message || "登入時發生未知錯誤。");
    }
  };

  return (
    <>
      <section>
        <h2>登入</h2>
        <div className="card">
          <input
            type="text"
            placeholder="帳號"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <br />
          <input
            type="password"
            placeholder="密碼"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <br />
          {error && <p style={{ color: 'red', fontSize: '0.9rem' }}>{error}</p>}
          <button onClick={handleLogin}>登入</button>
          <Link to="/">
            <button style={{backgroundColor: '#6c757d', marginTop: '0.5rem'}}>返回首頁</button>
          </Link>
        </div>
      </section>
    </>
  );
}

export default Login;
