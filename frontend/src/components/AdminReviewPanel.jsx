import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getAllClaims, getCourses, getGrades, reviewClaim, setRule } from "../api/verifyApi";
import StatusBadge from "./StatusBadge";

export default function AdminReviewPanel() {
  const { token } = useAuth();
  const [courses, setCourses] = useState([]);
  const [grades, setGrades] = useState([]);
  const [claims, setClaims] = useState([]);
  const [filter, setFilter] = useState("pending");
  const [choices, setChoices] = useState({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadCourses() {
    try {
      const [courseList, gradeList] = await Promise.all([getCourses(token), getGrades(token)]);
      setCourses(courseList);
      setGrades(gradeList);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadClaims(status = filter) {
    try {
      setClaims(await getAllClaims(token, status));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadCourses();
  }, []);

  useEffect(() => {
    loadClaims(filter);
  }, [filter]);

  async function handleSaveRule(course) {
    const minGrade = choices[course.course_id] ?? course.min_grade;
    setError("");
    setMessage("");
    if (!minGrade) {
      setError("Choose a minimum grade first");
      return;
    }
    try {
      await setRule(token, course.course_id, minGrade);
      setMessage(`Rule saved for ${course.course_code}: minimum ${minGrade}`);
      await Promise.all([loadCourses(), loadClaims()]);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleReview(claim, status) {
    const reason = window.prompt(`Reason for ${status} (optional):`, "");
    if (reason === null) return; // the admin pressed Cancel
    setError("");
    setMessage("");
    try {
      await reviewClaim(token, claim.id, status, reason.trim() || null);
      setMessage(`Claim from ${claim.tutor_name} for ${claim.course_code} is now ${status}`);
      await loadClaims();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <div className="panel">
        <h2>Grade rules</h2>
        <p className="muted">
          A tutor needs at least this grade to teach the course. Changing a rule decides the
          claims that are still pending. It does not change claims that are already decided.
        </p>
        <table>
          <thead>
            <tr>
              <th>Course</th>
              <th>Minimum grade</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {courses.map((course) => (
              <tr key={course.course_id}>
                <td>
                  {course.course_code} - {course.course_title}
                </td>
                <td>
                  <select
                    value={choices[course.course_id] ?? course.min_grade ?? ""}
                    onChange={(e) =>
                      setChoices({ ...choices, [course.course_id]: e.target.value })
                    }
                  >
                    <option value="">No rule</option>
                    {grades.map((g) => (
                      <option key={g} value={g}>
                        {g}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <button className="small" onClick={() => handleSaveRule(course)}>
                    Save
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="panel">
        <h2>Tutor applications</h2>
        <label>
          Show
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="">All</option>
          </select>
        </label>
        {claims.length === 0 ? (
          <p className="muted">No applications here.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Tutor</th>
                <th>Course</th>
                <th>Grade</th>
                <th>Status</th>
                <th>Reason</th>
                <th>Override</th>
              </tr>
            </thead>
            <tbody>
              {claims.map((claim) => (
                <tr key={claim.id}>
                  <td>
                    {claim.tutor_name}
                    <br />
                    <span className="muted">{claim.tutor_email}</span>
                  </td>
                  <td>{claim.course_code}</td>
                  <td>{claim.claimed_grade}</td>
                  <td>
                    <StatusBadge status={claim.status} />
                  </td>
                  <td>{claim.reason}</td>
                  <td>
                    <div className="actions">
                      <button
                        className="small"
                        disabled={claim.status === "approved"}
                        onClick={() => handleReview(claim, "approved")}
                      >
                        Approve
                      </button>
                      <button
                        className="small danger"
                        disabled={claim.status === "rejected"}
                        onClick={() => handleReview(claim, "rejected")}
                      >
                        Reject
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}