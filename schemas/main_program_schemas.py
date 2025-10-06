from typing import List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MainProgramColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    DESCRIPTION = "description"
    STATUS = "status"
    PROCESS_RATING = "process_rating"
    CREATED_AT = "created_at"


class NewMainProgram(BaseModel):
    name: str
    description: str


class CreateMainProgram(NewMainProgram):
    id: str
    engagement: str


class UpdateMainProgram(NewMainProgram):
    pass


class UpdateMainProgramProcessRating(BaseModel):
    process_rating: str


class ReadMainProgramOnPRCM(BaseModel):
    name: str
