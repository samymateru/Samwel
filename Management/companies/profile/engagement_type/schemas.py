from pydantic import BaseModel
from typing import Optional, List

class EngagementType(BaseModel):
    values: Optional[List[str]]

