import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function DashboardView() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="card">
      <h1>Welcome, {user.name}</h1>
      <p>Email: {user.email}</p>
      <p>Role: {user.role}</p>
      {user.role === "student" && (
        <p>
          <Link to="/find-tutor">Find a tutor</Link>
        </p>
      )}
      {user.role === "student" && (
        <p>
          <Link to="/sessions">Book a session</Link>
        </p>
      )}
      {user.role === "tutor" && (
        <p>
          <Link to="/profile">My tutor profile</Link>
        </p>
      )}
      {user.role === "tutor" && (
        <p>
          <Link to="/my-slots">My session slots</Link>
        </p>
      )}
      {(user.role === "tutor" || user.role === "admin") && (
        <p>
          <Link to="/verify">Tutor course verification</Link>
        </p>
      )}
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}