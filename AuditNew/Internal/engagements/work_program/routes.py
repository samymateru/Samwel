from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from utils import  get_db_connection
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage


router = APIRouter(prefix="/engagements")

@router.post("/main_program/{engagement_id}", response_model=ResponseMessage)
def create_new_main_program(
        engagement_id: int,
        program: MainProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_main_program(db, program=program, engagement_id=engagement_id)
        return ResponseMessage(detail="Main program added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/main_program/{engagement_id}", response_model=List[MainProgram])
def fetch_main_program(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_main_program(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/main_program/{program_id}", response_model=ResponseMessage)
def update_main_program(
        program_id: int,
        program: MainProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_main_program(db, program=program, program_id=program_id)
        return {"detail": "Main program successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/main_program/{program_id}", response_model=ResponseMessage)
def delete_main_program(
        program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_work_program(connection=db, id=program_id, table="main_program", resource="Main program")
        return {"detail": "Main program deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/sub_program/{program_id}", response_model=ResponseMessage)
def create_new_sub_program(
        program_id: int,
        sub_program: NewSubProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_new_sub_program(db, sub_program=sub_program, program_id=program_id)
        return {"detail": "Sub program added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/sub_program/{program_id}", response_model=List[SubProgram])
def fetch_sub_program(
        program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_sub_program(db, program_id=program_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/sub_program/{program_id}", response_model=ResponseMessage)
def update_sub_program(
        program_id: int,
        sub_program: SubProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_sub_program(db, sub_program=sub_program, program_id=program_id)
        return {"detail": "Sub program successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/sub_program/{sub_program_id}", response_model=ResponseMessage)
def delete_sub_program(
        sub_program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_work_program(connection=db, id=sub_program_id, table="sub_program", resource="Sub program")
        return {"detail": "Sub program deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/sub_program/evidence/{sub_program_id}", response_model=ResponseMessage)
def create_new_sub_program_evidence(
        sub_program_id: int,
        attachment: UploadFile = File(...),
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        evidence = SubProgramEvidence(
            attachment=attachment.filename
        )
        add_new_sub_program_evidence(db, evidence=evidence, sub_program_id=sub_program_id)
        return {"detail": "Evidence added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/sub_program/evidence/{sub_program_id}", response_model=List[SubProgramEvidence])
def fetch_engagement_letter(
        sub_program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_sub_program_evidence(db, column="sub_program", value=sub_program_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)




















