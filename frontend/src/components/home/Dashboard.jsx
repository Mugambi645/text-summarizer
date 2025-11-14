import React from "react";
import { getAccessToken, setAccessToken } from "../api";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Dashboard() {
  const navigate = useNavigate();

  const logout = async () => {
    try {
      await axios.post(
        "http://localhost:8000/logout/",
        {},
        { withCredentials: true }
      );
    } catch (err) {
      console.error("Logout error", err);
    }
    // clear access token in memory
    setAccessToken(null);
    navigate("/login");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Welcome to the Dashboard!</h1>
      <p>This is a protected page, accessible only after login.</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
