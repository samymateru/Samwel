from pydantic import BaseModel
from typing import Optional, List

class ControlType(BaseModel):
    values: Optional[List[str]]
