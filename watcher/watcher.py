import configparser
import requests
import time
import datetime
import json
from pathlib import Path

CONFIG = {
    "local_path": r"C:\Users\Public\Documents\Steam\CODEX\367520\achievements.ini",  # ruta real de logros
    "server": "http://127.0.0.1:8000/upload",
    "user_id": "cristhian",
    "game": "Hollow Knight",
    "poll_seconds": 15,
    "sent_log": "sent_logros.json",  # archivo local donde se guardan los logros ya enviados
}


def load_sent():
    """Carga el registro de logros enviados (si existe)."""
    if Path(CONFIG["sent_log"]).exists():
        try:
            with open(CONFIG["sent_log"], "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_sent(data):
    """Guarda el registro de logros enviados."""
    with open(CONFIG["sent_log"], "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


print(f"Watcher iniciado — monitoreando: {CONFIG['local_path']}")
sent = load_sent()

while True:
    p = Path(CONFIG["local_path"])
    if p.exists():
        parser = configparser.ConfigParser()
        parser.read(p, encoding="utf-8")

        for section in parser.sections():
            if section == "SteamAchievements":
                continue

            a = parser[section]
            unlocked = a.get("Achieved", "0") == "1"
            ts = int(a.get("UnlockTime", "0") or 0)
            unlock_time = (
                datetime.datetime.utcfromtimestamp(ts).isoformat() if ts > 0 else None
            )

            # Solo enviamos si es nuevo o cambió su estado
            prev = sent.get(section)
            if prev and prev.get("unlocked") == unlocked:
                continue  # ya fue enviado y no cambió

            data = {
                "user_id": CONFIG["user_id"],
                "game": CONFIG["game"],
                "ach_id": section,
                "name": section,  # opcional
                "description": f"Logro del juego {CONFIG['game']}",
                "unlocked": unlocked,
                "unlocked_at": unlock_time,
            }

            try:
                r = requests.post(CONFIG["server"], json=data, timeout=5)
                if r.status_code == 200:
                    sent[section] = {"unlocked": unlocked, "unlocked_at": unlock_time}
                    save_sent(sent)
                    print(f"✔ Logro nuevo enviado: {section}")
                else:
                    print(f"⚠ Error al enviar {section}: {r.status_code} -> {r.text}")
            except Exception as e:
                print("❌ Error de conexión:", e)
    else:
        print("⚠ No se encontró el archivo de logros.")

    time.sleep(CONFIG["poll_seconds"])
