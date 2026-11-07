import { apiRequest } from "./client";

// ----- tutor -----
export const createSlot = (token, { course, startsAt, durationMinutes, capacity }) =>
  apiRequest("/api/sessions/slots", {
    method: "POST",
    token,
    body: {
      course,
      starts_at: startsAt,
      duration_minutes: durationMinutes,
      capacity,
    },
  });

export const getMySlots = (token) => apiRequest("/api/sessions/my-slots", { token });

export const cancelSlot = (token, slotId) =>
  apiRequest(`/api/sessions/slots/${slotId}/cancel`, { method: "POST", token });

export const completeSlot = (token, slotId) =>
  apiRequest(`/api/sessions/slots/${slotId}/complete`, { method: "POST", token });

// ----- student -----
export const getOpenSlots = (token, course) =>
  apiRequest(`/api/sessions/slots${course ? `?course=${encodeURIComponent(course)}` : ""}`, {
    token,
  });

export const bookSlot = (token, slotId) =>
  apiRequest(`/api/sessions/slots/${slotId}/book`, { method: "POST", token });

export const getMyBookings = (token) => apiRequest("/api/sessions/my-bookings", { token });

export const cancelBooking = (token, bookingId) =>
  apiRequest(`/api/sessions/bookings/${bookingId}/cancel`, { method: "POST", token });