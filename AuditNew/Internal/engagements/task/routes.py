from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.task.databases import *

router = APIRouter(prefix="/task")

@router.post("/{engagement_id}")
def create_new_task(
        engagement_id: int,
        task: Task,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_task(db, task=task, engagement_id=engagement_id)
        return {"detail": "Task added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/{task_id}", response_model=ResponseMessage)
def update_task(
        task_id: int,
        task: Task,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_task(db, task=task, task_id=task_id)
        return {"detail": "Task successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{task_id}", response_model=ResponseMessage)
def delete_task(
        task_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return {"detail": "Task deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)