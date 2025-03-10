from fastapi import APIRouter, Depends, HTTPException
from schema import ResponseMessage, CurrentUser
from utils import get_db_connection, get_current_user
from Management.companies.profile.opinion_rating.databases import *
from typing import List

router = APIRouter(prefix="/profile/opinion_rating")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_opinion_rating(
        company_id: int,
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
            company_id=company_id)
        return {"detail": "Opinion rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/company/{company_id}", response_model=List[OpinionRating])
def fetch_company_opinion_rating(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_opinion_rating(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{opinion_rating_id}", response_model=ResponseMessage)
def fetch_opinion_rating(
        opinion_rating_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_opinion_rating(db, opinion_rating_id=opinion_rating_id)
        return data
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