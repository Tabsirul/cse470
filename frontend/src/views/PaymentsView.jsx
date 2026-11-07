import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getMyPayments } from "../api/paymentApi";
import StatusBadge from "../components/StatusBadge";
import { formatTime } from "../utils";

const MEANING = {
  held: "Held safely until the session is done",
  released: "Paid to the tutor",
  refunded: "Returned to you",
};

export default function PaymentsView() {
  const { token, user } = useAuth();
  const [payments, setPayments] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getMyPayments(token)
      .then(setPayments)
      .catch((err) => setError(err.message));
  }, [token]);

  if (user.role !== "student") {
    return (
      <div className="page">
        <p className="muted">This page is for students.</p>
      </div>
    );
  }

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      <h1>My payments</h1>
      {error && <p className="error">{error}</p>}
      <div className="panel">
        {payments.length === 0 ? (
          <p className="muted">
            No payments yet. Pay for a booking on the <Link to="/sessions">booking page</Link>.
          </p>
        ) : (
          payments.map((payment) => (
            <div className="result" key={payment.payment_id}>
              <div>
                <p>
                  <strong>{payment.course_code}</strong> with {payment.tutor_name}{" "}
                  <StatusBadge status={payment.status} />
                </p>
                <p className="muted">
                  {formatTime(payment.starts_at)} &middot; {MEANING[payment.status]}
                </p>
                <p className="muted">
                  {payment.method} ****{payment.account_last4} &middot; Ref {payment.reference}
                </p>
              </div>
              <div className="score">
                <strong>{payment.amount}</strong>
                <span className="muted">taka</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}