from pydantic import BaseModel
from typing import List, Optional

class AchievementIn(BaseModel):
    ach_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    unlocked: bool
    unlocked_at: Optional[str] = None
    meta: Optional[dict] = None

class UploadPayload(BaseModel):
    user_id: str
    game: str
    achievements: List[AchievementIn]
