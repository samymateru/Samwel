from AuditNew.Internal.engagements.attachments.schemas import AttachmentSections
from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, UploadFile, File, Query
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.planning.databases import *
from schema import ResponseMessage

router = APIRouter(prefix="/engagements")

@router.get("/PRCM/{engagement_id}", response_model=List[PRCM])
async def fetch_prcm(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_prcm(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/PRCM/{prcm_id}", response_model=ResponseMessage)
async def update_prcm(
        prcm_id: str,
        prcm: PRCM,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_prcm(connection=db, prcm=prcm, prcm_id=prcm_id)
        return ResponseMessage(detail="PRCM updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/PRCM/{prcm_id}", response_model=ResponseMessage)
async def delete_prcm(
        prcm_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_prcm(connection=db, prcm_id=prcm_id)
        return ResponseMessage(detail="PRCM deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/summary_audit_program/{engagement_id}", response_model=List[SummaryAuditProgramResponse])
async def fetch_summary_of_audit_program(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_summary_audit_program(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/engagement_letter/{engagement_id}", response_model=List[EngagementLetter])
async def fetch_engagement_letter(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_letter(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/engagement_letter/{engagement_id}", response_model=ResponseMessage)
async def create_new_engagement_letter(
        engagement_id: str,
        attachment: UploadFile = File(...),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        letter = EngagementLetter(
            name=attachment.filename,
            value="",
            size=attachment.size,
            extension=attachment.content_type
        )
        await add_engagement_letter(db, letter=letter, engagement_id=engagement_id)
        return ResponseMessage(detail="Letter added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/PRCM/{engagement_id}", response_model=ResponseMessage)
async def create_new_prcm(
        engagement_id: str,
        prcm: PRCM,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_engagement_prcm(db, prcm=prcm, engagement_id=engagement_id)
        return ResponseMessage(detail="PRCM added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/summary_audit_program/{engagement_id}", response_model=ResponseMessage)
async def create_new_summary_of_audit_program(
        engagement_id: str,
        work_program: PlanningWorkProgram,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await work_program_(
            connection=db,
            work_program=work_program,
            engagement_id=engagement_id
            )
        return ResponseMessage(detail="Audit program added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/summary_audit_program")
async def updating_summary_audit_finding(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_summary_audit_finding(connection=db)
        return ResponseMessage(detail="Audit program updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/summary_audit_program/{summary_audit_program_id}", response_model=ResponseMessage)
async def delete_summary_of_audit_program(
        summary_audit_program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_summary_audit_program(connection=db, summary_audit_program_id=summary_audit_program_id)
        return ResponseMessage(detail="Summary of audit program deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/planning_procedures/{engagement_id}", response_model=ResponseMessage)
async def create_new_planning_procedure(
        engagement_id: str,
        procedure: NewPlanningProcedure,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_planning_procedure(db, procedure=procedure, engagement_id=engagement_id)
        return ResponseMessage(detail="Planning procedure added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/planning_procedures/{engagement_id}", response_model=List[StandardTemplate])
async def fetch_planning_procedures(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_planning_procedures(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/planning_procedures/{procedure_id}", response_model=ResponseMessage)
async def update_planning_procedure(
        procedure_id: str,
        std_template: StandardTemplate,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_planning_procedure(db, std_template=std_template, procedure_id=procedure_id)
        return ResponseMessage(detail="Planning procedure updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



###############################################################################
@router.put("/procedure/{procedure_id}", response_model=ResponseMessage)
async def save_procedure(
        procedure_id: str,
        procedure: SaveProcedure,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await save_procedure_(connection=db, procedure=procedure, procedure_id=procedure_id, resource=procedure.type)
        return ResponseMessage(detail="Planning procedure saved successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/procedure/prepare/{procedure_id}", response_model=ResponseMessage)
async def prepare_procedure(
        procedure_id: str,
        procedure: PreparedReviewedBy,
        resource: str = Query(...),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await prepare_std_template(connection=db, procedure=procedure, procedure_id=procedure_id, resource=resource)
        return ResponseMessage(detail="Planning procedure prepared successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/procedure/review/{procedure_id}", response_model=ResponseMessage)
async def review_procedure(
        procedure_id: str,
        procedure: PreparedReviewedBy,
        resource: str = Query(...),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await review_std_template(connection=db, procedure=procedure, procedure_id=procedure_id, resource=resource)
        return ResponseMessage(detail="Planning procedure reviewed successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)