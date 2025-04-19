from pydantic import BaseModel
from typing import Optional, List

class ControlEffectivenessRating(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]