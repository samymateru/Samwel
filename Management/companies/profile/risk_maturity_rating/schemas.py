from pydantic import BaseModel
from typing import Optional, List

class RiskMaturityRating(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]

