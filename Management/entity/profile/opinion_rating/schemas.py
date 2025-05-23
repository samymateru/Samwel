from pydantic import BaseModel
from typing import Optional, List

class OpinionRating(BaseModel):
    values: Optional[List[str]]
