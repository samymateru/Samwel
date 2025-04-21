from pydantic import BaseModel
from typing import Optional


class Risk(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    rating: Optional[str]
