import { apiRequest } from "./client";

export const getGrades = (token) => apiRequest("/api/verify/grades", { token });

export const getCourses = (token) => apiRequest("/api/verify/courses", { token });

export const getMyClaims = (token) => apiRequest("/api/verify/my-claims", { token });

export const submitClaim = (token, courseId, claimedGrade) =>
  apiRequest("/api/verify/claims", {
    method: "POST",
    token,
    body: { course_id: courseId, claimed_grade: claimedGrade },
  });

export const getAllClaims = (token, status) =>
  apiRequest(`/api/verify/claims${status ? `?status=${status}` : ""}`, { token });

export const setRule = (token, courseId, minGrade) =>
  apiRequest(`/api/verify/courses/${courseId}/rule`, {
    method: "PUT",
    token,
    body: { min_grade: minGrade },
  });

export const reviewClaim = (token, claimId, status, reason) =>
  apiRequest(`/api/verify/claims/${claimId}`, {
    method: "PATCH",
    token,
    body: { status, reason },
  });