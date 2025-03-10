from pydantic import BaseModel
from typing import Optional

class IssueImplementation(BaseModel):
    id: Optional[int] = None
    name: str