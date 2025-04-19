from pydantic import BaseModel
from typing import Optional, List

class IssueSource(BaseModel):
    company: Optional[str]
    values: Optional[List[str]]


