from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from AuditNew.Internal.follow_up.databases import add_new_follow_up
from AuditNew.Internal.follow_up.schemas import NewFollowUp
from schema import ResponseMessage
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response
from typing import List, Optional


router = APIRouter(prefix="/follow_up")
@router.post("/{module_id}", response_model=ResponseMessage)
async def create_new_follow_up(
        module_id: str,
        name: str = Form(...),
        engagement_ids: Optional[List[str]] = Form(None),
        issue_ids: Optional[List[str]] = Form(None),
        attachment: Optional[UploadFile] = File(None),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await add_new_follow_up(
            connection=connection,
            follow_up=NewFollowUp
            (
            name=name,
            engagement_ids=engagement_ids,
            issue_ids=issue_ids,
            attachment= attachment.filename if attachment is not None else None
            ),
            module_id=module_id,
            user_id=""
        )
        if data is None:
            raise HTTPException(status_code=400, detail="Failed to create new follow")
        return ResponseMessage(detail="Follow Up Successfully Created")