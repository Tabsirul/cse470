import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AdminReviewPanel from "../components/AdminReviewPanel";
import TutorClaimsPanel from "../components/TutorClaimsPanel";

export default function PrereqVerifyView() {
  const { user } = useAuth();

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>Tutor course verification</h1>
      {user.role === "admin" && <AdminReviewPanel />}
      {user.role === "tutor" && <TutorClaimsPanel />}
      {user.role === "student" && (
        <p className="muted">This page is for tutors and admins.</p>
      )}
    </div>
  );
}