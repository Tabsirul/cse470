import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getCourses } from "../api/verifyApi";
import { searchTutors } from "../api/tutorApi";
import Stars from "../components/Stars";

export default function TutorMatchView() {
  const { token } = useAuth();
  const [activeTab, setActiveTab] = useState("syllabus");
  const [courses, setCourses] = useState([]);
  
  // Base Search States (F1)
  const [course, setCourse] = useState("");
  const [maxRate, setMaxRate] = useState("");
  const [minRating, setMinRating] = useState("");

  const [freeSession, setFreeSession] = useState(false);
  const [syllabusQuery, setSyllabusQuery] = useState("");
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
      const params = {
        course,
        maxRate: activeTab === "base" ? maxRate : "",
        minRating: activeTab === "base" ? minRating : "",
        syllabusQuery: activeTab === "syllabus" ? syllabusQuery : "",
        freeSession: activeTab === "base" ? freeSession : false,
      };

      const list = await searchTutors(token, params);
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

      {/* Sub-navigation tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <button
          type="button"
          onClick={() => {
            setActiveTab("base");
            setFreeSession(false);
            setResults(null);
          }}
          style={{
            padding: "10px 18px",
            borderRadius: "6px",
            border: "1px solid #cbd5e1",
            fontWeight: activeTab === "base" ? "bold" : "500",
            backgroundColor: activeTab === "base" ? "#2563eb" : "#f1f5f9",
            color: activeTab === "base" ? "#ffffff" : "#334155",
            cursor: "pointer",
          }}
        >
          Standard Search
        </button>
        <button
          type="button"
          onClick={() => {
            setActiveTab("syllabus");
            setFreeSession(false);
            setResults(null);
          }}
          style={{
            padding: "10px 18px",
            borderRadius: "6px",
            border: "1px solid #cbd5e1",
            fontWeight: activeTab === "syllabus" ? "bold" : "500",
            backgroundColor: activeTab === "syllabus" ? "#2563eb" : "#f1f5f9",
            color: activeTab === "syllabus" ? "#ffffff" : "#334155",
            cursor: "pointer",
          }}
        >
          Search by Syllabus Topics
        </button>
      </div>

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

            {activeTab === "syllabus" ? (
              <label>
                Syllabus Topic Needs
                <input
                  type="text"
                  placeholder="e.g. Midterm topics, Lab 2 requirements, Assignment modules..."
                  value={syllabusQuery}
                  onChange={(e) => setSyllabusQuery(e.target.value)}
                  required
                />
              </label>
            ) : (
              <>
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
              </>
            )}
          </div>

          {activeTab === "base" && (
            <label className="check">
              <input
                type="checkbox"
                checked={freeSession}
                onChange={(e) => setFreeSession(e.target.checked)}
              />
              Only tutors with a free session
            </label>
          )}

          <button type="submit" disabled={loading} style={{ marginTop: "15px" }}>
            {loading
              ? "Searching..."
              : activeTab === "syllabus"
              ? "Find tutors for this topic"
              : "Find tutors"}
          </button>
        </form>
      </div>

      {results !== null && (
        <div className="panel">
          <h2>
            Tutors for {searchedCourse}{" "}
            {activeTab === "syllabus" && syllabusQuery ? `(Topic Need: "${syllabusQuery}")` : ""}
          </h2>
          {results.length === 0 ? (
            <p className="muted">
              {activeTab === "syllabus"
                ? "No tutors found covering those specific exam or lab syllabus topics for this course."
                : "No tutor matches found for your budget, rating or free session filters."}
            </p>
          ) : (
            results.map((tutor, index) => (
              <div className="result" key={tutor.tutor_id}>
                <div>
                  <p>
                    <span className="rank">#{index + 1}</span> <strong>{tutor.tutor_name}</strong>
                  </p>
                  <p className="muted">
                    Grade in {searchedCourse}: {tutor.grade} &middot; {tutor.hourly_rate} taka per
                    hour
                  </p>
                  <p>
                    {tutor.rating === null ? (
                      <span className="muted">New tutor, no reviews yet</span>
                    ) : (
                      <>
                        <Stars value={tutor.rating} /> {tutor.rating} ({tutor.review_count}{" "}
                        {tutor.review_count === 1 ? "review" : "reviews"}){" "}
                        <Link to={`/tutors/${tutor.tutor_id}/reviews`}>Read reviews</Link>
                      </>
                    )}
                  </p>
                  <div className="panel">
                    <p>
                      {tutor.free_sessions > 0 ? (
                        <Link to={`/sessions?course=${searchedCourse}`}>
                          {tutor.free_sessions} free {tutor.free_sessions === 1 ? "session" : "sessions"}{" "}
                          - book now
                        </Link>
                      ) : (
                        <span className="muted">No free session right now</span>
                      )}
                    </p>
                    {tutor.bio && <p>{tutor.bio}</p>}

                    {tutor.syllabus_topics && (
                      <div
                        style={{
                          marginTop: "8px",
                          fontSize: "0.85em",
                          color: "#1e293b",
                          backgroundColor: "#f8fafc",
                          padding: "6px 10px",
                          borderRadius: "4px",
                          border: "1px solid #e2e8f0",
                        }}
                      >
                        <strong style={{ color: "#0f172a" }}>Covered Syllabus Topics:</strong>{" "}
                        {tutor.syllabus_topics}
                      </div>
                    )}
                  </div>
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