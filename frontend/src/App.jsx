import { useEffect, useState } from "react";
import { fetchAchievements } from "./api";

export default function App() {
  const [user, setUser] = useState("cristhian"); // cambia si quieres
  const [game, setGame] = useState("Hollow Knight");
  const [ach, setAch] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAchievements(user, game);
      setAch(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // auto-refresh cada 20s
    const t = setInterval(load, 20000);
    return () => clearInterval(t);
  }, [user, game]);

  return (
    <div className="app">
      <header className="header">
        <h1>HydraCloudLite</h1>
        <div className="controls">
          <label>
            Usuario
            <input value={user} onChange={e => setUser(e.target.value)} />
          </label>
          <label>
            Juego
            <input value={game} onChange={e => setGame(e.target.value)} />
          </label>
          <button onClick={load}>Recargar</button>
        </div>
      </header>

      <main>
        {loading && <div className="note">Cargando logros…</div>}
        {error && <div className="error">Error: {error}</div>}

        {!loading && !error && (
          <>
            <div className="summary">
              <div>Total: {ach.length}</div>
              <div>
                Desbloqueados: {ach.filter(a => a.unlocked).length}
              </div>
              <div>
                %:{" "}
                {ach.length === 0
                  ? "0"
                  : Math.round(
                      (ach.filter(a => a.unlocked).length / ach.length) * 100
                    )}
                %
              </div>
            </div>

            <div className="list">
              {ach.map(a => (
                <div
                  key={a.ach_id}
                  className={"item " + (a.unlocked ? "unlocked" : "locked")}
                >
                  <div className="left">
                    <div className="title">{a.name || a.ach_id}</div>
                    {a.description && (
                      <div className="desc">{a.description}</div>
                    )}
                  </div>
                  <div className="right">
                    <div className="status">
                      {a.unlocked ? "✅" : "🔒"}
                    </div>
                    <div className="date">{a.unlocked_at || ""}</div>
                  </div>
                </div>
              ))}
              {ach.length === 0 && (
                <div className="note">No hay logros para este usuario/juego.</div>
              )}
            </div>
          </>
        )}
      </main>

      <footer className="footer">
        HydraCloudLite — local server
      </footer>
    </div>
  );
}
