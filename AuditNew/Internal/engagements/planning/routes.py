from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
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

@router.put("/PRCM/{prcm_id}", response_model=ResponseMessage)
def update_prcm(
        prcm_id: int,
        prcm: PRCM,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_prcm(connection=db, prcm=prcm, prcm_id=prcm_id)
        return ResponseMessage(detail="PRCM updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/PRCM/{prcm_id}", response_model=ResponseMessage)
def delete_prcm(
        prcm_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_prcm(connection=db, prcm_id=prcm_id)
        return ResponseMessage(detail="PRCM deleted successfully")
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

@router.post("/engagement_letter/{engagement_id}", response_model=ResponseMessage)
def create_new_engagement_letter(
        engagement_id: int,
        name: str = Form(...),
        date_attached: datetime = Form(...),
        attachment: UploadFile = File(...),
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        letter = EngagementLetter(
            name=name,
            date_attached=date_attached,
            attachment=attachment.filename
        )
        add_engagement_letter(db, letter=letter, engagement_id=engagement_id)
        return {"detail": "Letter added successfully"}
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

@router.put("/summary_audit_program/{summary_audit_program_id}")
def updating_summary_audit_finding(
        summary_audit_program_id: int,
        summary: SummaryAuditProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_summary_audit_finding(connection=db, summary=summary, summary_audit_program_id=summary_audit_program_id)
        return {"detail": "Audit program updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/summary_audit_program/{summary_audit_program_id}", response_model=ResponseMessage)
def delete_summary_of_audit_program(
        summary_audit_program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_summary_audit_program(connection=db, summary_audit_program_id=summary_audit_program_id)
        return ResponseMessage(detail="Summary of audit program deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/planning_procedures/{engagement_id}", response_model=ResponseMessage)
def create_new_planning_procedure(
        engagement_id: int,
        procedure: NewPlanningProcedure,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_planning_procedure(db, procedure=procedure, engagement_id=engagement_id)
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

@router.put("/planning_procedures/{procedure_id}", response_model=ResponseMessage)
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
        return ResponseMessage(detail="Planning procedure updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

