from pydantic import BaseModel
from typing import Optional, List

class Rating(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    magnitude: Optional[int]

class RiskRating(BaseModel):
    values: Optional[List[Rating]]

