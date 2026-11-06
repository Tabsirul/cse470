import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getEarnings } from "../api/paymentApi";
import StatusBadge from "../components/StatusBadge";
import { formatTime } from "../utils";

export default function TutorEarningsView() {
  const { token, user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getEarnings(token)
      .then(setData)
      .catch((err) => setError(err.message));
  }, [token]);

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
      <h1>My earnings</h1>
      {error && <p className="error">{error}</p>}
      {data && (
        <>
          <div className="panel totals">
            <div>
              <strong>{data.released_total} taka</strong>
              <span className="muted">paid to you</span>
            </div>
            <div>
              <strong>{data.pending_total} taka</strong>
              <span className="muted">waiting for sessions to finish</span>
            </div>
          </div>
          <div className="panel">
            <h2>Payments</h2>
            {data.items.length === 0 ? (
              <p className="muted">No payments yet.</p>
            ) : (
              data.items.map((item) => (
                <div className="result" key={item.payment_id}>
                  <div>
                    <p>
                      <strong>{item.course_code}</strong> with {item.student_name}{" "}
                      <StatusBadge status={item.status} />
                    </p>
                    <p className="muted">
                      {formatTime(item.starts_at)} &middot; student paid {item.amount} &middot;
                      StudyBuddy fee {item.platform_fee}
                    </p>
                  </div>
                  <div className="score">
                    <strong>{item.tutor_amount}</strong>
                    <span className="muted">taka to you</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}