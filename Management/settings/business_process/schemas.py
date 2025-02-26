from pydantic import BaseModel
from typing import Optional, List

class BusinessProcess(BaseModel):
    process_name: str
    code: str
    id: int
    sub_process_name: List[str]

class NewBusinessProcess(BaseModel):
    name: str

class UpdateBusinessProcess(BaseModel):
    id: int
    name: Optional[str] = None

class DeleteBusinessProcess(BaseModel):
    id: int