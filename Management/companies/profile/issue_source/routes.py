from fastapi import APIRouter, Depends, HTTPException
from schema import ResponseMessage, CurrentUser
from utils import get_db_connection, get_current_user
from Management.companies.profile.issue_source.databases import *
from Management.companies.profile.issue_source.schemas import *


router = APIRouter(prefix="/profile/issue_source")

@router.post("/", response_model=ResponseMessage)
def create_issue_source(
        issue_source: IssueSource,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_issue_source(
            db,
            issue_source=issue_source,
            company_id=user.company_id)
        return {"detail": "Issue source added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/")
def fetch_company_issue_source(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_issue_source(db, company_id=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{issue_source_id}")
def fetch_issue_source(
        issue_source_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_issue_source(db, issue_source_id=issue_source_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{issue_source_id}", response_model=ResponseMessage)
def update_issue_source(
        issue_source_id: int,
        issue_source: IssueSource,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_issue_source(
            db,
            issue_source=issue_source,
            issue_source_id=issue_source_id)
        return {"detail": "Issue source updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{issue_source_id}", response_model=ResponseMessage)
def remove_issue_source(
        issue_source_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_issue_source(db, issue_source_id=issue_source_id)
        return {"detail": "Issue source deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)