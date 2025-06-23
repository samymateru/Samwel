from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class MainProgram(BaseModel):
    id: Optional[str] = None
    name: Optional[str]

class SubProgram(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    title: Optional[str]
    brief_description: Optional[str]
    audit_objective: Optional[str]
    test_description: Optional[str]
    test_type: Optional[str]
    sampling_approach: Optional[str]
    results_of_test: Optional[str]
    observation: Optional[str]
    extended_testing: Optional[bool]
    extended_procedure: Optional[str]
    extended_results: Optional[str]
    effectiveness: Optional[str]
    reviewed_by: Optional[User]
    prepared_by: Optional[User]
    conclusion: Optional[str]


class Procedure(BaseModel):
    procedure_id: Optional[str] = None
    procedure_title: Optional[str] = None
    reference: Optional[str] = None

class WorkProgram(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    procedures: List[Procedure]

class SubProgramEvidence(BaseModel):
    id: Optional[str] = None
    attachment: Optional[str]

class NewSubProgram(BaseModel):
    title: str

class SaveWorkProgramProcedure(BaseModel):
    brief_description: Optional[str]
    audit_objective: Optional[str]
    test_description: Optional[str]
    test_type: Optional[str]
    sampling_approach: Optional[str]
    results_of_test: Optional[str]
    observation: Optional[str]
    extended_testing: Optional[bool]
    extended_procedure: Optional[str]
    extended_results: Optional[str]
    effectiveness: Optional[str]
    conclusion: Optional[str]

class RiskControl(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_objective: Optional[str]
    control_type: Optional[str]
    residue_risk: Optional[str] = None

class PreparedReviewedBy(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime] = datetime.now()

class AddSummaryAuditProgram(BaseModel):
    prcm_id: Optional[str]
    procedure_id: Optional[str]





