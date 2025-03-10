from pydantic import BaseModel
from typing import Optional

class OpinionRating(BaseModel):
    id: Optional[int] = None
    name: str
