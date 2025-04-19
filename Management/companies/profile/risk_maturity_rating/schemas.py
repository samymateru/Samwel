from pydantic import BaseModel
from typing import Optional, List

class RiskMaturityRating(BaseModel):
    values: Optional[List[str]]

