from fastapi import APIRouter, Depends, Query
from schemas.engagement_administration_profile_schemas import NewEngagementAdministrationProfile
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/engagement_administration_profile")

@router.post("/{engagement_id}")
async def create_new_engagement_administration_profile(
        profile: NewEngagementAdministrationProfile,
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        print(profile)


@router.get("/{engagement_id}")
async def fetch_engagement_administration_profile(
        module_id: str,
        filters: str =  Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/{profile_id}")
async def update_engagement_administration_profile(
        profile_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


