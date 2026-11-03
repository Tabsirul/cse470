const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiRequest(path, { method = "GET", body, token } = {}) {
  const headers = {};
  if (body) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(readError(data));
  }
  return data;
}

function readError(data) {
  if (!data || !data.detail) return "Something went wrong";
  if (typeof data.detail === "string") return data.detail;
  // Validation errors (422) come as a list of messages
  return data.detail.map((item) => item.msg).join(". ");
}