from pydantic import BaseModel
from typing import Optional, List

class OpinionRating(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]
