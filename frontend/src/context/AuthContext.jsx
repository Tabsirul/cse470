import { createContext, useContext, useEffect, useState } from "react";
import { apiRequest } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("token")));

  // When the page opens with a saved token, ask the backend who this is.
  useEffect(() => {
    if (!token) return;
    apiRequest("/api/auth/me", { token })
      .then(setUser)
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, [token]);

  function saveSession(data) {
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
    setUser(data.user);
  }

  async function login(email, password) {
    const data = await apiRequest("/api/auth/login", {
      method: "POST",
      body: { email, password },
    });
    saveSession(data);
  }

  async function register(name, email, password, role) {
    const data = await apiRequest("/api/auth/register", {
      method: "POST",
      body: { name, email, password, role },
    });
    saveSession(data);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}