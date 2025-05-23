from pydantic import BaseModel
from typing import Optional, List

class Rating(BaseModel):
    name: Optional[str]
    magnitude: Optional[int]

class RiskRating(BaseModel):
    values: Optional[List[Rating]]

