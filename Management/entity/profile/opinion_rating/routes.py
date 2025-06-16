from fastapi import APIRouter, Depends, HTTPException
from schema import ResponseMessage, CurrentUser
from utils import get_db_connection, get_current_user, get_async_db_connection
from Management.entity.profile.opinion_rating.databases import *
from typing import List

router = APIRouter(prefix="/profile/opinion_rating")

@router.post("/", response_model=ResponseMessage)
def create_opinion_rating(
        opinion_rating: OpinionRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_opinion_rating(
            db,
            opinion_rating=opinion_rating,
            company_id=user.entity_id)
        return {"detail": "Opinion rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{entity_id}", response_model=OpinionRating)
async def fetch_company_opinion_rating(
        entity_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_opinion_rating(db, company_id=entity_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Opinion rating not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{opinion_rating_id}", response_model=ResponseMessage)
def update_opinion_rating(
        opinion_rating_id: int,
        opinion_rating: OpinionRating,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_opinion_rating(
            db,
            opinion_rating=opinion_rating,
            opinion_rating_id=opinion_rating_id)
        return {"detail": "Opinion rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{opinion_rating_id}", response_model=ResponseMessage)
def remove_opinion_rating(
        opinion_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        delete_opinion_rating(db, opinion_rating_id=opinion_rating_id)
        return {"detail": "Opinion rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)