const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return response.json();
}

export function fetchParks({ category = "", search = "" } = {}) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (search) params.set("search", search);
  const query = params.toString();
  return request(`/parks/${query ? `?${query}` : ""}`);
}

export function fetchParkForecast(slug) {
  return request(`/parks/${encodeURIComponent(slug)}/forecast/`);
}
