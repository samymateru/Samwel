from pydantic import BaseModel
from typing import Optional, List

class ControlWeaknessRating(BaseModel):
     company: Optional[str]
     values: Optional[List[str]]





