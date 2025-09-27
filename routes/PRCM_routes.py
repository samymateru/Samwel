from fastapi import APIRouter, Depends

from models.PRCM_models import create_new_prcm_model, get_prcm_model, update_prcm_model, delete_prcm_model, \
    get_summary_audit_program_model, remove_prcm_to_program_model
from schema import ResponseMessage
from schemas.PRCM_schemas import NewPRCM, UpdatePRCM
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/PRCM/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_new_prcm(
        engagement_id: str,
        prcm: NewPRCM,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_prcm_model(
            connection=connection,
            engagement_id=engagement_id,
            prcm=prcm
        )

        return await return_checker(
            data=results,
            passed="PRCM Successfully Created",
            failed="Failed Creating  PRCM"
        )


@router.get("/PRCM/{engagement_id}")
async def fetch_engagement_prcm(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_prcm_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data




@router.get("/summary_audit_program/{engagement_id}")
async def fetch_summary_audit_program(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_summary_audit_program_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data



@router.put("/PRCM/{prcm_id}")
async def update_engagement_prcm(
        prcm_id: str,
        prcm: UpdatePRCM,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_prcm_model(
            connection=connection,
            prcm=prcm,
            prcm_id=prcm_id
        )

        return await return_checker(
            data=results,
            passed="PRCM Successfully Updated",
            failed="Failed Updating  PRCM"
        )


@router.delete("/PRCM/{prcm_id}")
async def delete_engagement_prcm(
        prcm_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_prcm_model(
            connection=connection,
            prcm_id=prcm_id
        )

        return await return_checker(
            data=results,
            passed="PRCM Successfully Deleted",
            failed="Failed Deleting  PRCM"
        )

@router.delete("/summary_audit_program/{summary_audit_program_id}")
async def delete_summary_audit_program(
        summary_audit_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_prcm_to_program_model(
            connection=connection,
            prcm_id=summary_audit_program_id
        )

        return await return_checker(
            data=results,
            passed="Summary Audit Program Successfully Deleted",
            failed="Failed Deleting Summary Audit Program"
        )


