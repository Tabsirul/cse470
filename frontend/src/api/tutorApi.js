import { apiRequest } from "./client";

export const getMyProfile = (token) => apiRequest("/api/tutors/me/profile", { token });

export const saveMyProfile = (token, hourlyRate, bio) =>
  apiRequest("/api/tutors/me/profile", {
    method: "PUT",
    token,
    body: { hourly_rate: hourlyRate, bio },
  });

export function searchTutors(token, { course, maxRate, minRating, syllabusQuery, freeSession }) {
  const params = new URLSearchParams({ course });
  if (maxRate) params.set("max_rate", maxRate);
  if (minRating) params.set("min_rating", minRating);
  if (syllabusQuery) params.set("syllabus", syllabusQuery);
  if (freeSession) params.set("free_session", "true");
  return apiRequest(`/api/tutors/search?${params.toString()}`, { token });
}