from pydantic import BaseModel
from typing import Optional, List

class IssueSource(BaseModel):
    values: Optional[List[str]]


