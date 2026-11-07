import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const LINKS = {
  student: [
    { to: "/find-tutor", title: "Find a tutor", text: "Search by course, budget and rating." },
    { to: "/sessions", title: "Book a session", text: "Book, pay for and review sessions." },
    { to: "/payments", title: "My payments", text: "See held, released and refunded payments." },
  ],
  tutor: [
    { to: "/profile", title: "My tutor profile", text: "Set your price and introduction." },
    { to: "/my-slots", title: "My session slots", text: "Offer one-to-one or group sessions." },
    { to: "/earnings", title: "My earnings", text: "See what you earned and what is waiting." },
    { to: "REVIEWS", title: "My reviews", text: "See your rating and comments." },
    {
      to: "/verify",
      title: "Tutor course verification",
      text: "Apply to tutor a course with your grade.",
    },
  ],
  admin: [
    {
      to: "/verify",
      title: "Tutor course verification",
      text: "Review applications and set grade rules.",
    },
  ],
};

export default function DashboardView() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const links = LINKS[user.role] ?? [];

  return (
    <div className="page">
      <h1>Welcome, {user.name}</h1>
      <p className="meta">
        Email: {user.email} &middot; Role: {user.role}
      </p>
      <div className="grid">
        {links.map((link) => (
          <Link
            key={link.title}
            className="tile"
            to={link.to === "REVIEWS" ? `/tutors/${user.id}/reviews` : link.to}
          >
            <strong>{link.title}</strong>
            <span>{link.text}</span>
          </Link>
        ))}
      </div>
      <button className="secondary" onClick={handleLogout}>
        Log out
      </button>
    </div>
  );
}
