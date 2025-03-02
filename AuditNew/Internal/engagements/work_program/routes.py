from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_current_user
from schema import CurrentUser


router = APIRouter(prefix="/engagements")

@router.post("/main_program/{engagement_id}")
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
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/sub_program/{program_id}")
def create_new_main_program(
        program_id: int,
        sub_program: SubProgram,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_sub_program(db, sub_program=sub_program, program_id=program_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/sub_program/issue/{sub_program_id}")
def create_new_issue(
        sub_program_id: int,
        issue: Issue,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_issue(db, issue=issue, sub_program_id=sub_program_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/sub_program/task/{sub_program_id}")
def create_new_task(
        sub_program_id: int,
        task: Task,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_task(db, task=task, sub_program_id=sub_program_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/sub_program/review_note/{sub_program_id}")
def create_new_review_note(
        sub_program_id: int,
        review_note: ReviewNote,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_review_note(db, review_note=review_note, sub_program_id=sub_program_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)