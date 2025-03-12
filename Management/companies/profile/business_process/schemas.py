from pydantic import BaseModel
from typing import List

class BusinessProcess(BaseModel):
    id: int
    process_name: str
    code: str
    sub_process_name: List[str]

class NewBusinessProcess(BaseModel):
    name: str
    code: str

class NewBusinessSubProcess(BaseModel):
    name: str