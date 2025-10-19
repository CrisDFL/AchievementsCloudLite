from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from .database import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    game = Column(String, index=True)
    ach_id = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime)
    meta = Column(JSON, nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game": self.game,
            "ach_id": self.ach_id,
            "name": self.name,
            "description": self.description,
            "unlocked": self.unlocked,
            "unlocked_at": self.unlocked_at.isoformat() if self.unlocked_at else None,
            "meta": self.meta,
        }
