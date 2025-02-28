from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.administration.schemas import *
from AuditNew.Internal.engagements.administration.databases import *

router = APIRouter(prefix="/engagements")

@router.get("/profile/{engagement_id}", response_model=EngagementProfile)
def fetch_engagement_profile(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_profile(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/policies/{engagement_id}", response_model=EngagementProfile)
def fetch_engagement_policies(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_profile(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/engagement_process/{engagement_id}", response_model=EngagementProfile)
def fetch_engagement_process(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_process(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/regulations/{engagement_id}", response_model=EngagementProfile)
def fetch_regulations(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_regulations(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

x = {
  "name": "Owner", # Role name
  "categories": [
    {
      "name": "Eaudit settings",
      "permissions": {
        "roles": ["view", "edit", "delete"],
        "profile": ["view", "edit", "delete"],
        "subscription": ["view", "edit", "delete"]
      }
    },
    {
      "name": "Planning",
      "permissions": {
        "Audit plan": ["view", "edit", "delete"],
        "procedures": ["view", "edit", "delete"]
      }
    },
    {
        "name": "Fieldwork",
        "permission": {
            "Summary": ["view", "edit", "delete"],
            "Procedures": ["view", "edit", "delete"]
        }
    }
  ]
}
