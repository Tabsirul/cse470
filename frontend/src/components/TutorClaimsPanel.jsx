import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getCourses, getGrades, getMyClaims, submitClaim } from "../api/verifyApi";
import StatusBadge from "./StatusBadge";

export default function TutorClaimsPanel() {
  const { token } = useAuth();
  const [courses, setCourses] = useState([]);
  const [grades, setGrades] = useState([]);
  const [claims, setClaims] = useState([]);
  const [courseId, setCourseId] = useState("");
  const [grade, setGrade] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function loadAll() {
    try {
      const [courseList, gradeList, claimList] = await Promise.all([
        getCourses(token),
        getGrades(token),
        getMyClaims(token),
      ]);
      setCourses(courseList);
      setGrades(gradeList);
      setClaims(claimList);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setSubmitting(true);
    try {
      const claim = await submitClaim(token, Number(courseId), grade);
      setMessage(`${claim.course_code}: ${claim.status}. ${claim.reason}`);
      setCourseId("");
      setGrade("");
      await loadAll();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <div className="panel">
        <h2>Apply to tutor a course</h2>
        {error && <p className="error">{error}</p>}
        {message && <p className="success">{message}</p>}
        <form onSubmit={handleSubmit}>
          <label>
            Course
            <select value={courseId} onChange={(e) => setCourseId(e.target.value)} required>
              <option value="">Choose a course</option>
              {courses.map((course) => (
                <option key={course.course_id} value={course.course_id}>
                  {course.course_code} - {course.course_title} (
                  {course.min_grade ? `minimum ${course.min_grade}` : "no rule yet"})
                </option>
              ))}
            </select>
          </label>
          <label>
            The grade you got in this course
            <select value={grade} onChange={(e) => setGrade(e.target.value)} required>
              <option value="">Choose a grade</option>
              {grades.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </label>
          <button type="submit" disabled={submitting}>
            {submitting ? "Sending..." : "Apply"}
          </button>
        </form>
      </div>

      <div className="panel">
        <h2>My applications</h2>
        {claims.length === 0 ? (
          <p className="muted">You have not applied for any course yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Course</th>
                <th>My grade</th>
                <th>Status</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {claims.map((claim) => (
                <tr key={claim.id}>
                  <td>{claim.course_code}</td>
                  <td>{claim.claimed_grade}</td>
                  <td>
                    <StatusBadge status={claim.status} />
                  </td>
                  <td>{claim.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}