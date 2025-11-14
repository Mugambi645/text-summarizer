import React, { useState } from "react";
import { login as doLogin } from "./auth";
import { setAccessToken } from "../api";
import { useNavigate } from "react-router-dom";

function Login() {
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    try {
      const access = await doLogin(u, p);
      setAccessToken(access);

      // Redirect to protected page
      navigate("/dashboard");  // change to any route you want
    } catch (err) {
      console.error("Login error", err);
      alert("Invalid username or password");
    }
  };

  return (
    <div>
      <input 
        value={u} 
        onChange={(e) => setU(e.target.value)} 
        placeholder="username"
      />

      <input 
        value={p}
        onChange={(e) => setP(e.target.value)} 
        type="password"
        placeholder="password"
      />

      <button onClick={submit}>Login</button>
    </div>
  );
}

export default Login;
