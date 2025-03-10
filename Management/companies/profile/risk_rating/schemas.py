from pydantic import BaseModel
from typing import Optional


class RiskRating(BaseModel):
    id: Optional[int] = None
    name: str
