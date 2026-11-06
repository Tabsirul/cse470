import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getMyProfile } from "../api/tutorApi";
import { cancelSlot, completeSlot, createSlot, getMySlots } from "../api/sessionApi";
import StatusBadge from "../components/StatusBadge";
import { formatTime } from "../utils";

export default function TutorSlotsView() {
  const { token, user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [slots, setSlots] = useState([]);
  const [course, setCourse] = useState("");
  const [startsAt, setStartsAt] = useState("");
  const [duration, setDuration] = useState("60");
  const [capacity, setCapacity] = useState("1");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);
  const [now] = useState(() => new Date());

  const loadSlots = useCallback(async () => {
    try {
      setSlots(await getMySlots(token));
    } catch (err) {
      setError(err.message);
    }
  }, [token]);

  useEffect(() => {
    getMyProfile(token)
      .then((profile) => setCourses(profile.approved_courses))
      .catch((err) => {
        if (err.status !== 404) setError(err.message);
      });
    loadSlots();
  }, [token, loadSlots]);

  async function handleCreate(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setSaving(true);
    try {
      await createSlot(token, {
        course,
        startsAt,
        durationMinutes: Number(duration),
        capacity: Number(capacity),
      });
      setMessage("Session added");
      await loadSlots();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleAction(action, slotId, done) {
    setError("");
    setMessage("");
    try {
      await action(token, slotId);
      setMessage(done);
      await loadSlots();
    } catch (err) {
      setError(err.message);
    }
  }

  if (user.role !== "tutor") {
    return (
      <div className="page">
        <p className="muted">This page is for tutors.</p>
      </div>
    );
  }

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>My session slots</h1>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <div className="panel">
        <h2>Offer a new session</h2>
        {courses.length === 0 ? (
          <p className="muted">
            You need a saved <Link to="/profile">profile</Link> and an approved course first.
          </p>
        ) : (
          <form onSubmit={handleCreate}>
            <div className="filters">
              <label>
                Course
                <select value={course} onChange={(e) => setCourse(e.target.value)} required>
                  <option value="">Choose a course</option>
                  {courses.map((code) => (
                    <option key={code} value={code}>
                      {code}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Start time
                <input
                  type="datetime-local"
                  value={startsAt}
                  onChange={(e) => setStartsAt(e.target.value)}
                  required
                />
              </label>
              <label>
                Length
                <select value={duration} onChange={(e) => setDuration(e.target.value)}>
                  <option value="30">30 minutes</option>
                  <option value="60">1 hour</option>
                  <option value="90">1.5 hours</option>
                  <option value="120">2 hours</option>
                </select>
              </label>
              <label>
                Seats (1 = one-to-one)
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={capacity}
                  onChange={(e) => setCapacity(e.target.value)}
                  required
                />
              </label>
            </div>
            <button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Add session"}
            </button>
          </form>
        )}
      </div>

      <div className="panel">
        <h2>My sessions</h2>
        {slots.length === 0 ? (
          <p className="muted">You have not offered any session yet.</p>
        ) : (
          slots.map((slot) => (
            <div className="result" key={slot.slot_id}>
              <div>
                <p>
                  <strong>{slot.course_code}</strong> &middot; {formatTime(slot.starts_at)}{" "}
                  <StatusBadge status={slot.status} />
                </p>
                <p className="muted">
                  {slot.duration_minutes} minutes &middot;{" "}
                  {slot.capacity === 1 ? "one-to-one" : `group of up to ${slot.capacity}`} &middot;{" "}
                  {slot.booked_count} booked, {slot.seats_left} free &middot; {slot.price} taka per
                  student
                </p>
              </div>
              {slot.status === "open" && (
                <div className="actions">
                  {new Date(slot.starts_at) <= now && slot.booked_count > 0 && (
                    <button
                      className="small"
                      onClick={() =>
                        handleAction(completeSlot, slot.slot_id, "Session marked as completed")
                      }
                    >
                      Mark completed
                    </button>
                  )}
                  <button
                    className="small danger"
                    onClick={() => handleAction(cancelSlot, slot.slot_id, "Session cancelled")}
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}