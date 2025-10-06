from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class SubProgramColumns(str, Enum):
    ID = "id"
    PROGRAM = "program"
    REFERENCE = "reference"
    TITLE = "title"
    BRIEF_DESCRIPTION = "brief_description"
    AUDIT_OBJECTIVE = "audit_objective"
    TEST_DESCRIPTION = "test_description"
    TEST_TYPE = "test_type"
    SAMPLING_APPROACH = "sampling_approach"
    RESULTS_OF_TEST = "results_of_test"
    OBSERVATION = "observation"
    EXTENDED_TESTING = "extended_testing"
    EXTENDED_PROCEDURE = "extended_procedure"
    EXTENDED_RESULTS = "extended_results"
    EFFECTIVENESS = "effectiveness"
    REVIEWED_BY = "reviewed_by"
    PREPARED_BY = "prepared_by"
    CONCLUSION = "conclusion"


class NewSubProgram(BaseModel):
    title: str


class ReviewPrepareUser(BaseModel):
    name: str
    email: str
    date_issued: datetime


class CreateSubProgram(NewSubProgram):
    id: str = None
    program: str
    reference: str = None
    title: str
    brief_description: str
    audit_objective: str
    test_description: str
    test_type: str
    sampling_approach: str
    results_of_test: str
    observation: str
    extended_testing: bool
    extended_procedure: str
    extended_results: str
    effectiveness: str
    reviewed_by: Optional[ReviewPrepareUser] = None
    prepared_by: Optional[ReviewPrepareUser] = None
    conclusion: str


class UpdateSubProgram(BaseModel):
    title: str
    brief_description: str
    audit_objective: str
    test_description: str
    test_type: str
    sampling_approach: str
    results_of_test: str
    observation: str
    extended_testing: bool
    extended_procedure: str
    extended_results: str
    effectiveness: str
    reviewed_by: Optional[ReviewPrepareUser] = None
    prepared_by: Optional[ReviewPrepareUser] = None
    conclusion: str


class ReadSubProgramOnPRCM(BaseModel):
    title: str