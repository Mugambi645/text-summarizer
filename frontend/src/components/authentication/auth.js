import axios from "axios";

export async function login(username, password) {
  const res = await axios.post("http://localhost:8000/api/auth/login/", {
    username, password
  }, { withCredentials: true }); // important: allow cookies
  // server set refresh cookie; we get access in the body
  return res.data.access; // caller should store in memory (context)
}
