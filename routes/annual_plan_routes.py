from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from models.annual_plan_models import register_new_annual_plan, get_module_annual_plans, get_annual_plan_details, \
    remove_annual_plan_partially, edit_annual_plan_details
from schema import ResponseMessage
from schemas.annual_plan_schemas import NewAnnualPlan, ReadAnnualPlan, UpdateAnnualPlan
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker
from datetime import datetime
from typing import List

router = APIRouter(prefix="/annual_plans")


@router.post("/{module_id}", status_code=201, response_model=ResponseMessage)
async def create_new_annual_plan(
        module_id: str,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        annual_plan = NewAnnualPlan(
            name=name,
            year=year,
            start=start,
            end=end,
            attachment=attachment.filename
        )

        results = await register_new_annual_plan(
            connection=connection,
            annual_plan=annual_plan,
            module_id=module_id
        )

        return await return_checker(
            data=results,
            passed="Annual Plan Successfully Created",
            failed="Failed Creating  Annual Plan"
        )


@router.get("/{module_id}", response_model=List[ReadAnnualPlan])
async def fetch_all_module_annual_plans(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_module_annual_plans(
            connection=connection,
            module_id=module_id
        )
        return data


@router.get("/single_plan/{annual_plan_id}", response_model=ReadAnnualPlan)
async def fetch_single_plan_data(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_annual_plan_details(
            connection=connection,
            annual_plan_id=annual_plan_id
        )


        if data is None:
            raise HTTPException(status_code=404, detail="Annual Plan Not Found")
        return data

@router.put("/{annual_plan_id}", response_model=ResponseMessage)
async def update_annual_plan_data(
        annual_plan_id: str,
        annual_plan: UpdateAnnualPlan,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await edit_annual_plan_details(
            connection=connection,
            annual_plan=annual_plan,
            annual_plan_id=annual_plan_id
        )

        return await return_checker(
            data=results,
            passed="Annual Plan Successfully Updated",
            failed="Failed Updating  Annual Plan"
        )


@router.delete("/{annual_plan_id}", response_model=ResponseMessage)
async def remove_annual_plan_data(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_annual_plan_partially(
            connection=connection,
            annual_plan_id=annual_plan_id
        )

        return await return_checker(
            data=results,
            passed="Annual Plan Successfully Deleted",
            failed="Failed Deleting  Annual Plan"
        )

