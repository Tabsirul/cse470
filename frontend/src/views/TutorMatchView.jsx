import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getCourses } from "../api/verifyApi";
import { searchTutors } from "../api/tutorApi";

export default function TutorMatchView() {
  const { token } = useAuth();
  const [courses, setCourses] = useState([]);
  const [course, setCourse] = useState("");
  const [maxRate, setMaxRate] = useState("");
  const [minRating, setMinRating] = useState("");
  const [results, setResults] = useState(null);
  const [searchedCourse, setSearchedCourse] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCourses(token)
      .then(setCourses)
      .catch((err) => setError(err.message));
  }, [token]);

  async function handleSearch(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const list = await searchTutors(token, { course, maxRate, minRating });
      setResults(list);
      setSearchedCourse(course);
    } catch (err) {
      setError(err.message);
      setResults(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>Find a tutor</h1>

      <div className="panel">
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSearch}>
          <div className="filters">
            <label>
              Course
              <select value={course} onChange={(e) => setCourse(e.target.value)} required>
                <option value="">Choose a course</option>
                {courses.map((c) => (
                  <option key={c.course_id} value={c.course_code}>
                    {c.course_code} - {c.course_title}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Most I can pay per hour (taka)
              <input
                type="number"
                min="1"
                placeholder="Any price"
                value={maxRate}
                onChange={(e) => setMaxRate(e.target.value)}
              />
            </label>
            <label>
              Lowest rating
              <select value={minRating} onChange={(e) => setMinRating(e.target.value)}>
                <option value="">Any rating</option>
                <option value="3">3 stars or more</option>
                <option value="3.5">3.5 stars or more</option>
                <option value="4">4 stars or more</option>
                <option value="4.5">4.5 stars or more</option>
              </select>
            </label>
          </div>
          <button type="submit" disabled={loading}>
            {loading ? "Searching..." : "Find tutors"}
          </button>
        </form>
      </div>

      {results !== null && (
        <div className="panel">
          <h2>Tutors for {searchedCourse}</h2>
          {results.length === 0 ? (
            <p className="muted">
              No tutor matches. Try a higher budget or a lower rating. Tutors with no reviews
              are hidden when you choose a lowest rating.
            </p>
          ) : (
            results.map((tutor, index) => (
              <div className="result" key={tutor.tutor_id}>
                <div>
                  <p>
                    <span className="rank">#{index + 1}</span> <strong>{tutor.tutor_name}</strong>
                  </p>
                  <p className="muted">
                    Grade in {searchedCourse}: {tutor.grade} &middot;{" "}
                    {tutor.rating === null ? "New tutor, no reviews yet" : `${tutor.rating} stars`}{" "}
                    &middot; {tutor.hourly_rate} taka per hour
                  </p>
                  {tutor.bio && <p>{tutor.bio}</p>}
                </div>
                <div className="score">
                  <strong>{tutor.score}</strong>
                  <span className="muted">match score</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}