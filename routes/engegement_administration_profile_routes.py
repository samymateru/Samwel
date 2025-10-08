from fastapi import APIRouter, Depends, HTTPException
from models.engagement_administration_profile_models import update_engagement_profile_model, \
    fetch_engagement_administration_profile_model, review_engagement_administration_profile_model, \
    prepare_engagement_administration_profile_model
from schemas.engagement_administration_profile_schemas import NewEngagementAdministrationProfile, \
    ReadEngagementAdministrationProfile, ReviewEngagementProfile, PrepareEngagementProfile
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")


@router.get("/profile/{engagement_id}", response_model=ReadEngagementAdministrationProfile)
async def fetch_engagement_administration_profile(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_engagement_administration_profile_model(
            connection=connection,
            engagement_id=engagement_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Engagement Profile Not Found")
        return data


@router.put("/profile/{engagement_id}")
async def update_engagement_administration_profile(
        profile: NewEngagementAdministrationProfile,
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_engagement_profile_model(
            connection=connection,
            profile=profile,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Profile Successfully Updated",
            failed="Failed Updating  Engagement Profile"
        )



@router.put("/review/{profile_id}")
async def review_engagement_administration_profile(
        profile_id: str,
        review: ReviewEngagementProfile,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await review_engagement_administration_profile_model(
            connection=connection,
            profile_id=profile_id,
            review=review
        )

        return await return_checker(
            data=results,
            passed="Engagement Profile Successfully Reviewed",
            failed="Failed Reviewing  Engagement Profile"
        )






@router.put("/prepare/{profile_id}")
async def prepare_engagement_administration_profile_status(
        profile_id: str,
        prepare: PrepareEngagementProfile,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await prepare_engagement_administration_profile_model(
            connection=connection,
            profile_id=profile_id,
            prepare=prepare
        )


        return await return_checker(
            data=results,
            passed="Engagement Profile Successfully Prepared",
            failed="Failed Preparing  Engagement Profile"
        )





