from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class NewModule(BaseModel):
    name: str
    description: str = None
    status: bool = True
    created_at: datetime = datetime.now()

class DeleteModule(BaseModel):
    id: str

class UpdateModule(BaseModel):
    id: str
    description: Optional[str] = None

