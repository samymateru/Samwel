from pydantic import BaseModel
from typing import Optional


class Risk(BaseModel):
    id: Optional[int] = None
    ref: Optional[str]
    name: Optional[str]
    rating: Optional[str]
