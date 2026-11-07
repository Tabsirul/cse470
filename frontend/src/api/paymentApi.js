import { apiRequest } from "./client";

export const payBooking = (token, bookingId, method, account) =>
  apiRequest(`/api/payments/bookings/${bookingId}/pay`, {
    method: "POST",
    token,
    body: { method, account },
  });

export const getMyPayments = (token) => apiRequest("/api/payments/my-payments", { token });

export const getEarnings = (token) => apiRequest("/api/payments/earnings", { token });