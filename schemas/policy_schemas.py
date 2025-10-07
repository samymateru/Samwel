from pydantic import BaseModel
from enum import Enum

from schemas.attachement_schemas import ReadAttachment


class PolicyColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    VERSION = "version"
    KEY_AREAS = "key_areas"



class NewPolicy(BaseModel):
    name: str
    version: str
    key_areas: str



class CreatePolicy(NewPolicy):
    id: str
    engagement: str



class UpdatePolicy(NewPolicy):
    pass



class BasePolicy(BaseModel):
    id: str
    engagement: str
    name: str
    version: str
    key_areas: str



class ReadPolicy(BasePolicy):
    attachment: ReadAttachment

