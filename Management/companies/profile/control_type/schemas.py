from pydantic import BaseModel
from typing import Optional, List

class ControlType(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]
