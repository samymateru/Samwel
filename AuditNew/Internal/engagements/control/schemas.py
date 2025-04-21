from pydantic import BaseModel
from typing import Optional

class Control(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    objective: Optional[str]
    type: Optional[str]