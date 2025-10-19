const BASE = import.meta.env.VITE_API || "http://localhost:8000";

export async function fetchAchievements(user, game) {
  const url = `${BASE}/user/${encodeURIComponent(user)}/game/${encodeURIComponent(game)}/achievements`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Error al obtener logros: " + res.status);
  return res.json();
}
