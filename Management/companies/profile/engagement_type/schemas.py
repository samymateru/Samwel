from pydantic import BaseModel
from typing import Optional, List

class EngagementType(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]

