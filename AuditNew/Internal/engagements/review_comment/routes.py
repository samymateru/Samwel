from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.review_comment.databases import *

router = APIRouter(prefix="/review_comment")

@router.post("/raise/{engagement_id}", response_model=ResponseMessage)
async def raise_review_comment(
        engagement_id: str,
        review_comment: NewReviewComment,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await raise_review_comment_(db, review_comment=review_comment, engagement_id=engagement_id)
        return ResponseMessage(detail="Review comment raised successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/raise/{review_comment_id}", response_model=ResponseMessage)
async def update_raised_review_comment(
        review_comment_id: str,
        review_comment: NewReviewComment,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return ResponseMessage(detail="Raised review comment updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/resolve/{review_comment_id}", response_model=ResponseMessage)
async def resolve_review_comment(
        review_comment_id: str,
        review_comment: ResolveReviewComment,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await resolve_review_comment_(connection=db, review_comment=review_comment, review_comment_id=review_comment_id)
        return ResponseMessage(detail="Review comment resolved successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{review_comment_id}", response_model=ResponseMessage)
async def delete_review_comment(
        review_comment_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_review_comment(connection=db, review_comment_id=review_comment_id)
        return ResponseMessage(detail="Review comment deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)