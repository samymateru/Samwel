from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.review_comment.databases import *

router = APIRouter(prefix="/review_comment")

@router.post("/{engagement_id}", response_model=ResponseMessage)
def create_new_review_comment(
        engagement_id: int,
        review_comment: NewReviewComment,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_new_review_comment(db, review_comment=review_comment, engagement_id=engagement_id)
        return {"detail": "Review comment added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{review_comment_id}", response_model=ResponseMessage)
def update_review_comment(
        review_comment_id: int,
        review_comment: ReviewComment,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_review_comment(db, review_comment=review_comment, review_comment_id=review_comment_id)
        return {"detail": "Review comment successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{review_comment_id}", response_model=ResponseMessage)
def delete_review_comment(
        review_comment_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        return {"detail": "Review comment deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)