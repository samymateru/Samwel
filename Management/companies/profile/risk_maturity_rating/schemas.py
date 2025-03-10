from pydantic import BaseModel
from typing import Optional

class RiskMaturityRating(BaseModel):
    id: Optional[int] = None
    name: str

