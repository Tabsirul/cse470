import { useCallback, useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getCourses } from "../api/verifyApi";
import { bookSlot, cancelBooking, getMyBookings, getOpenSlots } from "../api/sessionApi";
import { payBooking } from "../api/paymentApi";
import { createReview } from "../api/reviewApi";
import Stars from "../components/Stars";
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
  const [payingId, setPayingId] = useState(null); // which booking has the pay form open
  const [method, setMethod] = useState("bkash");
  const [account, setAccount] = useState("");
  const [reviewingId, setReviewingId] = useState(null); // which booking has the review form open
  const [stars, setStars] = useState(5);
  const [comment, setComment] = useState("");

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

  async function handlePay(event, bookingId) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await payBooking(token, bookingId, method, account);
      setMessage("Payment received. We hold it safely and pay the tutor after the session.");
      setPayingId(null);
      setAccount("");
    } catch (err) {
      setError(err.message);
    }
    await load();
  }

  async function handleReview(event, bookingId) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await createReview(token, bookingId, stars, comment);
      setMessage("Thank you for your review");
      setReviewingId(null);
      setStars(5);
      setComment("");
    } catch (err) {
      setError(err.message);
    }
    await load();
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
          bookings.map((booking) => {
            const canPay =
              booking.status === "booked" &&
              booking.slot.status === "open" &&
              (booking.payment_status === null || booking.payment_status === "refunded");
            const canReview =
              booking.status === "booked" &&
              booking.slot.status === "completed" &&
              booking.payment_status === "released" &&
              booking.review_rating === null;
            return (
              <div className="result" key={booking.booking_id}>
                <div>
                  <p>
                    <strong>{booking.slot.course_code}</strong> with {booking.slot.tutor_name}{" "}
                    <StatusBadge status={booking.status} />{" "}
                    {booking.payment_status && <StatusBadge status={booking.payment_status} />}
                  </p>
                  <p className="muted">
                    {formatTime(booking.slot.starts_at)} &middot; {booking.slot.duration_minutes}{" "}
                    minutes &middot; {booking.slot.price} taka
                  </p>
                  {booking.review_rating !== null && (
                    <p className="muted">
                      Your review: <Stars value={booking.review_rating} />
                    </p>
                  )}
                  {reviewingId === booking.booking_id && (
                    <form className="reviewform" onSubmit={(e) => handleReview(e, booking.booking_id)}>
                      <div className="starpicker">
                        {[1, 2, 3, 4, 5].map((n) => (
                          <button
                            type="button"
                            key={n}
                            className={n <= stars ? "star on" : "star"}
                            onClick={() => setStars(n)}
                            aria-label={`${n} stars`}
                          >
                            ★
                          </button>
                        ))}
                      </div>
                      <textarea
                        rows="3"
                        maxLength="500"
                        placeholder="How was the session? (optional)"
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                      />
                      <button type="submit" className="small">
                        Send review
                      </button>
                    </form>
                  )}
                  {payingId === booking.booking_id && (
                    <form className="payform" onSubmit={(e) => handlePay(e, booking.booking_id)}>
                      <select value={method} onChange={(e) => setMethod(e.target.value)}>
                        <option value="bkash">bKash (sandbox)</option>
                        <option value="nagad">Nagad (sandbox)</option>
                      </select>
                      <input
                        type="tel"
                        placeholder="01XXXXXXXXX"
                        value={account}
                        onChange={(e) => setAccount(e.target.value)}
                        required
                      />
                      <button type="submit" className="small">
                        Pay {booking.slot.price} taka
                      </button>
                      <p className="muted">
                        Sandbox: no real money moves. A number ending in 0000 is declined, so you
                        can test a failure.
                      </p>
                    </form>
                  )}
                </div>
                <div className="actions">
                  {canReview && reviewingId !== booking.booking_id && (
                    <button className="small" onClick={() => setReviewingId(booking.booking_id)}>
                      Leave a review
                    </button>
                  )}
                  {canPay && payingId !== booking.booking_id && (
                    <button className="small" onClick={() => setPayingId(booking.booking_id)}>
                      Pay now
                    </button>
                  )}
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
              </div>
            );
          })
        )}
        <p className="muted">
          You can cancel up to 2 hours before the start. A payment you made is refunded in full.
        </p>
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