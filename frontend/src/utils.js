// Shows a time from the server (like 2026-11-10T15:00:00) as "10 Nov 2026, 3:00 pm"
export function formatTime(iso) {
  return new Date(iso).toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
}