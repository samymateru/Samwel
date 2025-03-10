from pydantic import BaseModel
from typing import Optional

class IssueSource(BaseModel):
    id: Optional[int] = None
    name: str


