from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from Management.companies.profile.issue_implementation.databases import *
from Management.companies.profile.issue_implementation.schemas import *
from typing import List
router = APIRouter(prefix="/profile/issue_implementation")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_issue_implementation(
        company_id: int,
        issue_implementation: IssueImplementation,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_issue_implementation(
            db,
            issue_implementation=issue_implementation,
            company_id=company_id)
        return {"detail": "Issue implementation added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/company/{company_id}", response_model=List[IssueImplementation])
def fetch_company_issue_implementation(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_issue_implementation(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{issue_implementation_id}", response_model=IssueImplementation)
def fetch_issue_implementation(
        issue_implementation_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_issue_implementation(db, issue_implementation_id=issue_implementation_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{issue_implementation_id}", response_model=ResponseMessage)
def update_issue_implementation(
        issue_implementation_id: int,
        issue_implementation: IssueImplementation,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_issue_implementation(
            db,
            issue_implementation=issue_implementation,
            issue_implementation_id=issue_implementation_id)
        return {"detail": "Issue implementation updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{issue_implementation_id}", response_model=ResponseMessage)
def remove_issue_implementation(
        issue_implementation_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_issue_implementation(db, issue_implementation_id=issue_implementation_id)
        return {"detail": "Issue implementation deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
