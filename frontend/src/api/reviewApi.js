import { apiRequest } from "./client";

export const createReview = (token, bookingId, rating, comment) =>
  apiRequest(`/api/reviews/bookings/${bookingId}`, {
    method: "POST",
    token,
    body: { rating, comment },
  });

export const getTutorReviews = (token, tutorId) =>
  apiRequest(`/api/reviews/tutors/${tutorId}`, { token });