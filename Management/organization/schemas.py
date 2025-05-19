from pydantic import BaseModel
from typing import Optional

class Organization(BaseModel):
    id: Optional[str] = None
    name: Optional[str]