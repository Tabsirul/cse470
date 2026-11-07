import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getTutorReviews } from "../api/reviewApi";
import Stars from "../components/Stars";
import { formatTime } from "../utils";

export default function TutorReviewsView() {
  const { token } = useAuth();
  const { tutorId } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getTutorReviews(token, tutorId)
      .then(setData)
      .catch((err) => setError(err.message));
  }, [token, tutorId]);

  return (
    <div className="page">
      <p>
        <Link to="/dashboard">&larr; Back to dashboard</Link>
      </p>
      {error && <p className="error">{error}</p>}
      {data && (
        <>
          <h1>Reviews for {data.tutor_name}</h1>
          <div className="panel summary">
            {data.count === 0 ? (
              <p className="muted">No reviews yet.</p>
            ) : (
              <>
                <div className="big">
                  <strong>{data.average}</strong>
                  <Stars value={data.average} />
                  <span className="muted">
                    {data.count} {data.count === 1 ? "review" : "reviews"}
                  </span>
                </div>
                <div className="bars">
                  {[5, 4, 3, 2, 1].map((star) => (
                    <div className="bar-row" key={star}>
                      <span>{star}★</span>
                      <div className="bar">
                        <div
                          className="bar-fill"
                          style={{ width: `${(data.stars[star] / data.count) * 100}%` }}
                        />
                      </div>
                      <span className="muted">{data.stars[star]}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
          {data.reviews.length > 0 && (
            <div className="panel">
              {data.reviews.map((review) => (
                <div className="result" key={review.review_id}>
                  <div>
                    <p>
                      <Stars value={review.rating} /> <strong>{review.student_name}</strong>
                    </p>
                    {review.comment && <p>{review.comment}</p>}
                    <p className="muted">
                      {review.course_code} &middot; {formatTime(review.created_at)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}