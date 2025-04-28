from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.task.databases import *

router = APIRouter(prefix="/task")

@router.post("/raise/{engagement_id}", response_model=ResponseMessage)
async def raise_new_task(
        engagement_id: str,
        task: NewTask,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await raise_task(db, task=task, engagement_id=engagement_id)
        return ResponseMessage(detail="Task raised successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/raise/{task_id}", response_model=ResponseMessage)
async def update_raised_task(
        task_id: str,
        task: NewTask,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return ResponseMessage(detail="Raised task updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/resolve/{task_id}", response_model=ResponseMessage)
async def resolve_task(
        task_id: str,
        task: ResolveTask,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await resolve_task_(connection=db, task=task, task_id=task_id)
        return ResponseMessage(detail="Task resolved successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/resolve/decision/{task_id}", response_model=ResponseMessage)
async def task_decision(
        task_id: str,
        task: TaskDecision,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await resolve_decision_(connection=db, task=task, task_id=task_id)
        return ResponseMessage(detail="Task decision passed successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{task_id}", response_model=ResponseMessage)
async def delete_task(
        task_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_task(connection=db, task_id=task_id)
        return ResponseMessage(detail="Task deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)