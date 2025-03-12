from pydantic import BaseModel
from typing import Optional


class EngagementType(BaseModel):
    id: Optional[int] = None
    name: str
