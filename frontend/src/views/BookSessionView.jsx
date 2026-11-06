import { useCallback, useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getCourses } from "../api/verifyApi";
import { bookSlot, cancelBooking, getMyBookings, getOpenSlots } from "../api/sessionApi";
import StatusBadge from "../components/StatusBadge";
import { formatTime } from "../utils";

export default function BookSessionView() {
  const { token, user } = useAuth();
  const [searchParams] = useSearchParams();
  const [courses, setCourses] = useState([]);
  const [course, setCourse] = useState(searchParams.get("course") ?? "");
  const [slots, setSlots] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const load = useCallback(async () => {
    try {
      const [openSlots, myBookings] = await Promise.all([
        getOpenSlots(token, course),
        getMyBookings(token),
      ]);
      setSlots(openSlots);
      setBookings(myBookings);
    } catch (err) {
      setError(err.message);
    }
  }, [token, course]);

  useEffect(() => {
    getCourses(token)
      .then(setCourses)
      .catch((err) => setError(err.message));
  }, [token]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleAction(action, id, done) {
    setError("");
    setMessage("");
    try {
      await action(token, id);
      setMessage(done);
    } catch (err) {
      setError(err.message);
    }
    await load(); // always refresh, so the seat counts are up to date
  }

  if (user.role !== "student") {
    return (
      <div className="page">
        <p className="muted">This page is for students.</p>
      </div>
    );
  }

  const myLiveSlotIds = new Set(
    bookings.filter((b) => b.status === "booked").map((b) => b.slot.slot_id),
  );

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>Book a session</h1>
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}

      <div className="panel">
        <h2>My bookings</h2>
        {bookings.length === 0 ? (
          <p className="muted">You have not booked a session yet.</p>
        ) : (
          bookings.map((booking) => (
            <div className="result" key={booking.booking_id}>
              <div>
                <p>
                  <strong>{booking.slot.course_code}</strong> with {booking.slot.tutor_name}{" "}
                  <StatusBadge status={booking.status} />
                </p>
                <p className="muted">
                  {formatTime(booking.slot.starts_at)} &middot; {booking.slot.duration_minutes}{" "}
                  minutes &middot; {booking.slot.price} taka
                </p>
              </div>
              {booking.can_cancel && (
                <button
                  className="small danger"
                  onClick={() =>
                    handleAction(cancelBooking, booking.booking_id, "Booking cancelled")
                  }
                >
                  Cancel
                </button>
              )}
            </div>
          ))
        )}
        <p className="muted">You can cancel up to 2 hours before the start.</p>
      </div>

      <div className="panel">
        <h2>Open sessions</h2>
        <label>
          Course
          <select value={course} onChange={(e) => setCourse(e.target.value)}>
            <option value="">All courses</option>
            {courses.map((c) => (
              <option key={c.course_id} value={c.course_code}>
                {c.course_code} - {c.course_title}
              </option>
            ))}
          </select>
        </label>
        {slots.length === 0 ? (
          <p className="muted">No open session for this choice yet.</p>
        ) : (
          slots.map((slot) => {
            const mine = myLiveSlotIds.has(slot.slot_id);
            return (
              <div className="result" key={slot.slot_id}>
                <div>
                  <p>
                    <strong>{slot.course_code}</strong> with {slot.tutor_name}
                  </p>
                  <p className="muted">
                    {formatTime(slot.starts_at)} &middot; {slot.duration_minutes} minutes &middot;{" "}
                    {slot.capacity === 1 ? "one-to-one" : "group"} &middot; {slot.seats_left} of{" "}
                    {slot.capacity} seats free &middot; {slot.price} taka
                  </p>
                </div>
                {mine ? (
                  <span className="muted">Booked</span>
                ) : (
                  <button
                    className="small"
                    disabled={slot.seats_left === 0}
                    onClick={() => handleAction(bookSlot, slot.slot_id, "Session booked")}
                  >
                    {slot.seats_left === 0 ? "Full" : "Book"}
                  </button>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
