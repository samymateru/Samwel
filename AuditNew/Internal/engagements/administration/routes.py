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
        data = get_engagement_profile(db, column="engagement", value=engagement_id)[0]
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/policies/{engagement_id}", response_model=Policy)
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

@router.get("/context/engagement_process/{engagement_id}", response_model=EngagementProcess)
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


@router.get("/staff/{engagement_id}", response_model=EngagementProfile)
def fetch_staff(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_staff(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/profile/{engagement_id}")
def create_engagement_profile(
        engagement_id: int,
        profile: EngagementProfile,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        delete_profile(db, engagement_id)
        add_engagement_profile(db, profile=profile, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/policies/{engagement_id}")
def create_engagement_profile(
        engagement_id: int,
        policy: Policy,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_policies(db, policy=policy, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/engagement_process/{engagement_id}")
def create_engagement_process(
        engagement_id: int,
        process: EngagementProcess,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_process(db, process=process, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/regulations/{engagement_id}")
def create_engagement_regulations(
        engagement_id: int,
        regulation: Regulations,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_regulations(db, regulation=regulation, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/staff/{engagement_id}")
def create_engagement_staff(
        engagement_id: int,
        staff: Staff,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_engagement_staff(db, staff=staff, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

