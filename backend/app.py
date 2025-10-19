from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal
from .models import Achievement

app = FastAPI(title="Hydra Cloud Lite API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- RUTAS ---

@app.get("/")
def root():
    return {"message": "API online"}


@app.get("/user/{user}/game/{game}/achievements")
def get_achievements(user: str, game: str, db: Session = Depends(get_db)):
    achievements = (
        db.query(Achievement)
        .filter(Achievement.user_id == user, Achievement.game == game)
        .all()
    )
    if not achievements:
        raise HTTPException(status_code=404, detail="No achievements found for this user/game")
    return [a.as_dict() for a in achievements]


# --- NUEVO ENDPOINT PARA SUBIR LOGROS DESDE EL WATCHER ---
@app.post("/upload")
async def upload_achievement(request: Request, db: Session = Depends(get_db)):
    """
    Recibe un JSON del watcher con los datos de un logro desbloqueado y lo guarda en la base de datos.
    Si el logro ya existe (por ach_id + user_id + game), lo actualiza.
    """

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    required_fields = ["user_id", "game", "ach_id", "name", "description"]
    if not all(k in data for k in required_fields):
        raise HTTPException(status_code=400, detail="Missing fields")

    existing = (
        db.query(Achievement)
        .filter(
            Achievement.user_id == data["user_id"],
            Achievement.game == data["game"],
            Achievement.ach_id == data["ach_id"],
        )
        .first()
    )

    if existing:
        # Si ya existe, lo actualizamos
        existing.unlocked = data.get("unlocked", True)
        existing.unlocked_at = datetime.utcnow()
    else:
        # Si no existe, lo creamos
        new_ach = Achievement(
            user_id=data["user_id"],
            game=data["game"],
            ach_id=data["ach_id"],
            name=data.get("name"),
            description=data.get("description"),
            unlocked=data.get("unlocked", True),
            unlocked_at=datetime.utcnow(),
            meta=data.get("meta", {}),
        )
        db.add(new_ach)

    db.commit()
    return {"status": "success", "message": "Achievement uploaded"}
