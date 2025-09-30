from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from models.policy_models import create_new_policy_model, update_engagement_policy_model, get_engagement_policies_model, \
    get_single_engagement_policy_model, delete_engagement_policy_model
from schema import ResponseMessage
from schemas.policy_schemas import NewPolicy, UpdatePolicy
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/context/policies/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_new_policy(
        engagement_id: str,
        name: str = Form(...),
        version: str = Form(...),
        key_areas: str = Form(...),
        attachment: UploadFile = File(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        policy = NewPolicy(
            name=name,
            version=version,
            key_areas=key_areas,
        )

        results = await create_new_policy_model(
            connection=connection,
            policy=policy,engagement_id=engagement_id

        )

        return await return_checker(
            data=results,
            passed="Policy Successfully Created",
            failed="Failed Creating  Policy"
        )


@router.put("/context/policies/{policy_id}", response_model=ResponseMessage)
async def update_engagement_policy(
        policy_id: str,
        name: str = Form(...),
        version: str = Form(...),
        key_areas: str = Form(...),
        attachment: UploadFile = File(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        policy = UpdatePolicy(
            name=name,
            version=version,
            key_areas=key_areas,
        )

        results = await update_engagement_policy_model(
            connection=connection,
            policy=policy,
            policy_id=policy_id

        )

        return await return_checker(
            data=results,
            passed="Policy Successfully Updated",
            failed="Failed Updating  Policy"
        )



@router.get("/context/policies/{engagement_id}")
async def get_engagement_policies(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_engagement_policies_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data



@router.get("/context/policies/single/{policy_id}")
async def get_single_engagement_policy(
        policy_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_single_engagement_policy_model(
            connection=connection,
            policy_id=policy_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Policy Not Found")

        return data




@router.delete("/context/policies/{policy_id}")
async def delete_single_engagement_policy(
        policy_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_engagement_policy_model(
            connection=connection,
            policy_id=policy_id
        )

        return await return_checker(
            data=results,
            passed="Policy Successfully Deleted",
            failed="Failed Deleting  Policy"
        )


