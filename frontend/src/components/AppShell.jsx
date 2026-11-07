import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import SiteFooter from "./SiteFooter";

// The frame around every page you see after logging in.
export default function AppShell({ children }) {
  const { user } = useAuth();

  return (
    <div className="site">
      <a className="skip" href="#main">
        Skip to content
      </a>
      <header className="topbar">
        <div className="wrap">
          <Link to="/dashboard" className="brand">
            StudyBuddy
          </Link>
          <span className="who">
            {user.name} &middot; {user.role}
          </span>
        </div>
      </header>
      <main id="main" className="app-main">
        {children}
      </main>
      <SiteFooter />
    </div>
  );
}
