from fastapi import APIRouter, Depends, UploadFile, File
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage


router = APIRouter(prefix="/engagements")

@router.post("/main_program/{engagement_id}", response_model=ResponseMessage)
async def create_new_main_program(
        engagement_id: str,
        program: MainProgram,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_new_main_program(db, program=program, engagement_id=engagement_id)
        return ResponseMessage(detail="Main program added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/main_program/{engagement_id}", response_model=List[MainProgram])
async def fetch_main_program(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_main_program(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/main_program/{program_id}", response_model=ResponseMessage)
async def update_main_program(
        program_id: str,
        program: MainProgram,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_main_program(db, program=program, program_id=program_id)
        return ResponseMessage(detail="Main program successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/work_program/{engagement_id}", response_model=List[WorkProgram])
async def fetch_work_program(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_work_program(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/main_program/{program_id}", response_model=ResponseMessage)
async def delete_main_program(
        program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_work_program(connection=db, id=program_id, table="main_program", resource="Main program")
        return ResponseMessage(detail="Main program deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/sub_program/{program_id}", response_model=ResponseMessage)
async def create_new_sub_program(
        program_id: str,
        sub_program: NewSubProgram,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_new_sub_program(db, sub_program=sub_program, program_id=program_id)
        return ResponseMessage(detail="Sub program added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/sub_program/{program_id}", response_model=List[SubProgram])
async def fetch_sub_program(
        program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_sub_program(db, program_id=program_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/sub_program/{sub_program_id}", response_model=ResponseMessage)
async def update_sub_program(
        sub_program_id: str,
        sub_program: SubProgram,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_sub_program(db, sub_program=sub_program, sub_program_id=sub_program_id)
        return ResponseMessage(detail="Sub program successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/sub_program/{sub_program_id}", response_model=ResponseMessage)
async def delete_sub_program(
        sub_program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_work_program(connection=db, id=sub_program_id, table="sub_program", resource="Sub program")
        return ResponseMessage(detail="Sub program deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/sub_program/evidence/{sub_program_id}", response_model=ResponseMessage)
async def create_new_sub_program_evidence(
        sub_program_id: str,
        attachment: UploadFile = File(...),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        evidence = SubProgramEvidence(
            attachment=attachment.filename
        )
        await add_new_sub_program_evidence(db, evidence=evidence, sub_program_id=sub_program_id)
        return {"detail": "Evidence added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/sub_program/evidence/{sub_program_id}", response_model=List[SubProgramEvidence])
async def fetch_engagement_letter(
        sub_program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_sub_program_evidence(db, sub_program_id=sub_program_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)




















