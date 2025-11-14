import { useState } from "react";
import axios from "axios";

export default function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "",
  });

  const [msg, setMsg] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/api/auth/register/",
        formData,
        { withCredentials: true }
      );

      setMsg("Registration successful! You can now log in.");
    } catch (err) {
      if (err.response?.data) {
        setMsg(JSON.stringify(err.response.data));
      } else {
        setMsg("Error registering user.");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Register</h2>

      <input
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
      />

      <input
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
      />

      <input
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
      />

      <input
        type="password"
        name="password2"
        placeholder="Confirm Password"
        value={formData.password2}
        onChange={handleChange}
      />

      <button onClick={handleSubmit}>Register</button>

      {msg && <p>{msg}</p>}
    </div>
  );
}
