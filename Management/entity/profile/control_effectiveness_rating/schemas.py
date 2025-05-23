from pydantic import BaseModel
from typing import Optional, List

class ControlEffectivenessRating(BaseModel):
    values: Optional[List[str]]