import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getMyProfile, saveMyProfile } from "../api/tutorApi";

export default function TutorProfileView() {
  const { token, user } = useAuth();
  const [hourlyRate, setHourlyRate] = useState("");
  const [bio, setBio] = useState("");
  const [courses, setCourses] = useState([]);
  const [hasProfile, setHasProfile] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    getMyProfile(token)
      .then((profile) => {
        setHourlyRate(String(profile.hourly_rate));
        setBio(profile.bio ?? "");
        setCourses(profile.approved_courses);
        setHasProfile(true);
      })
      .catch((err) => {
        // 404 only means "no profile yet", so it is not an error for the page
        if (err.status !== 404) setError(err.message);
      });
  }, [token]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setSaving(true);
    try {
      const profile = await saveMyProfile(token, Number(hourlyRate), bio);
      setCourses(profile.approved_courses);
      setHasProfile(true);
      setMessage("Profile saved");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>My tutor profile</h1>

      {user.role !== "tutor" ? (
        <p className="muted">This page is for tutors.</p>
      ) : (
        <>
          <div className="panel">
            <h2>About me</h2>
            {error && <p className="error">{error}</p>}
            {message && <p className="success">{message}</p>}
            <form onSubmit={handleSubmit}>
              <label>
                Price per hour (taka)
                <input
                  type="number"
                  min="1"
                  max="10000"
                  value={hourlyRate}
                  onChange={(e) => setHourlyRate(e.target.value)}
                  required
                />
              </label>
              <label>
                A short introduction (optional)
                <textarea
                  rows="4"
                  maxLength="1000"
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                />
              </label>
              <button type="submit" disabled={saving}>
                {saving ? "Saving..." : "Save profile"}
              </button>
            </form>
          </div>

          <div className="panel">
            <h2>Courses I can be found for</h2>
            {!hasProfile ? (
              <p className="muted">Save your profile first.</p>
            ) : courses.length === 0 ? (
              <p className="muted">
                None yet. Students can only find you for courses where your application is
                approved. Apply on the <Link to="/verify">verification page</Link>.
              </p>
            ) : (
              <p>{courses.join(", ")}</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}