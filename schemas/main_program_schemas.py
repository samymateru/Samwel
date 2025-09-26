from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MainProgramColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    STATUS = "status"
    PROCESS_RATING = "process_rating"
    CREATED_AT = "created_at"


class NewMainProgram(BaseModel):
    name: str


class CreateMainProgram(NewMainProgram):
    id: str
    engagement: str


class UpdateMainProgram(NewMainProgram):
    pass


class UpdateMainProgramProcessRating(BaseModel):
    process_rating: str