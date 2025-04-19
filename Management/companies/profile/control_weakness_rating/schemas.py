from pydantic import BaseModel
from typing import Optional, List

class ControlWeaknessRating(BaseModel):
     values: Optional[List[str]]





