from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.planning.schemas import *
from AuditNew.Internal.engagements.planning.databases import *
from schema import ResponseMessage

router = APIRouter(prefix="/engagements")


@router.get("/PRCM/{engagement_id}", response_model=List[PRCM])
def fetch_prcm(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_prcm(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/summary_audit_program/{engagement_id}", response_model=List[SummaryAuditProgram])
def fetch_summary_of_audit_program(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_summary_audit_program(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/engagement_letter/{engagement_id}", response_model=List[EngagementLetter])
def fetch_engagement_letter(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_letter(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/engagement_letter/{engagement_id}")
def create_new_engagement_letter(
        engagement_id: int,
        letter: EngagementLetter,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_letter(db, letter=letter, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/PRCM/{engagement_id}", response_model=ResponseMessage)
def create_new_prcm(
        engagement_id: int,
        prcm: PRCM,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_prcm(db, prcm=prcm, engagement_id=engagement_id)
        return {"detail": "PRCM added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/summary_audit_program/{engagement_id}", response_model=ResponseMessage)
def create_new_summary_of_audit_program(
        engagement_id: int,
        summary: SummaryAuditProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_summary_audit_program(db, summary=summary, engagement_id=engagement_id)
        return {"detail": "Audit program added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/planning_procedures/{engagement_id}", response_model=ResponseMessage)
def create_new_planning_procedure(
        engagement_id: int,
        std_template: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_planning_procedure(db, std_template=std_template, engagement_id=engagement_id)
        return {"detail": "Planning procedure added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/planning_procedures/{engagement_id}", response_model=List[StandardTemplate])
def fetch_planning_procedures(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_planning_procedures(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/planning_procedures/{procedure_id}")
def update_planning_procedure(
        procedure_id: int,
        std_template: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_planning_procedure(db, std_template=std_template, procedure_id=procedure_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)