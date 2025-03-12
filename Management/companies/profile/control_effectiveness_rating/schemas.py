from pydantic import BaseModel
from typing import Optional

class ControlEffectivenessRating(BaseModel):
    id: Optional[int]
    name: str