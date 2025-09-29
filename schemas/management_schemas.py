from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ManagementColumns(str, Enum):
    MANAGEMENT_ID = "management_id"
    ORGANIZATION_ID = "organization_id"
    NAME = "name"
    EMAIL ="email"
    TITLE = "title"
    CREATED_AT = "created_at"



class NewManagement(BaseModel):
    name: str
    email: str
    title: str



class UpdateManagement(NewManagement):
    pass



class CreatedManagement(BaseModel):
    management_id: str
    organization_id: str
    name: str
    email: str
    title: str
    created_at: datetime



class ReadManagement(CreatedManagement):
    pass

