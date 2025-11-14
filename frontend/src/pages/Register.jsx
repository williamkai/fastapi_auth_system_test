import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/authService";

function Register() {
  const navigate = useNavigate();

  // 必填欄位
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  // 選填欄位
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [gender, setGender] = useState("");
  const [birthday, setBirthday] = useState("");

  const handleRegister = async () => {
    if (password !== confirm) {
      alert("密碼與確認密碼不一致！");
      return;
    }
    if (!username || !password) {
      alert("帳號和密碼為必填欄位！");
      return;
    }

    const userData = {
      username,
      password, // 後端需要的是原始密碼，它會自己進行雜湊
      full_name: fullName,
      email,
      phone,
      gender,
      birthday: birthday || null, // 如果生日為空字串，傳送 null
    };

    try {
      const result = await registerUser(userData);
      alert(`使用者 ${result.username} 註冊成功！將為您導向登入頁面。`);
      navigate("/login"); // 註冊成功後導向到登入頁
    } catch (error) {
      alert(`註冊失敗：${error.message}`);
    }
  };

  return (
    <>
      <section>
        <h2>註冊新帳戶</h2>
        <div className="card">
          {/* --- 必填資訊 --- */}
          <h3>必填資訊</h3>
          <input
            type="text"
            placeholder="帳號*"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="密碼*"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="確認密碼*"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />

          <div className="separator" style={{ margin: "1.5rem auto" }}></div>

          {/* --- 選填資訊 --- */}
          <h3>基本資料 (選填)</h3>
          <input
            type="text"
            placeholder="全名"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
          <input
            type="email"
            placeholder="電子郵件"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="tel"
            placeholder="電話"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
          <select value={gender} onChange={(e) => setGender(e.target.value)} style={{width: '100%', maxWidth: '314px', padding: '0.6rem'}}>
            <option value="">選擇性別</option>
            <option value="male">男性</option>
            <option value="female">女性</option>
            <option value="other">其他</option>
          </select>
          <input
            type="date"
            placeholder="生日"
            value={birthday}
            onChange={(e) => setBirthday(e.target.value)}
            style={{colorScheme: 'dark'}}
          />
          
          <br />
          <button onClick={handleRegister}>註冊</button>
          <Link to="/">
            <button style={{backgroundColor: '#6c757d', marginTop: '0.5rem'}}>返回首頁</button>
          </Link>
        </div>
      </section>
    </>
  );
}

export default Register;
