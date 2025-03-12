from pydantic import BaseModel
from typing import Optional

class ControlType(BaseModel):
    id: Optional[int] = None
    name: str
