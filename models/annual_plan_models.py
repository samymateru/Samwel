from psycopg import AsyncConnection

from core.tables import Tables
from schemas.annual_plan_schemas import NewAnnualPlan, CreateAnnualPlan, AnnualPlanStatus, AnnualPlanColumns, \
    UpdateAnnualPlan, RemoveAnnualPlanPartially
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def register_new_annual_plan(
        connection: AsyncConnection,
        annual_plan: NewAnnualPlan,
        module_id: str
):
    with exception_response():
        __annual_plan__ = CreateAnnualPlan(
            id=get_unique_key(),
            module=module_id,
            reference="",
            name=annual_plan.name,
            year=annual_plan.year,
            attachment=annual_plan.attachment,
            start=annual_plan.start,
            end=annual_plan.end,
            status=AnnualPlanStatus.PENDING,
            creator="",
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ANNUAL_PLANS.value)
            .values(__annual_plan__)
            .check_exists({AnnualPlanColumns.NAME.value: annual_plan.name})
            .check_exists({AnnualPlanColumns.MODULE.value: module_id})
            .returning(AnnualPlanColumns.ID.value)
            .execute()
        )

        return builder

async def get_module_annual_plans(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ANNUAL_PLANS.value)
            .where(AnnualPlanColumns.MODULE.value, module_id)
            .fetch_all()
        )

        return builder


async def get_annual_plan_details(
        connection: AsyncConnection,
        annual_plan_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ANNUAL_PLANS.value)
            .where(AnnualPlanColumns.ID.value, annual_plan_id)
            .fetch_one()
        )

        return builder


async def edit_annual_plan_details(
        connection: AsyncConnection,
        annual_plan: UpdateAnnualPlan,
        annual_plan_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ANNUAL_PLANS.value)
            .values(annual_plan)
            .check_exists({AnnualPlanColumns.ID.value: annual_plan_id})
            .where({AnnualPlanColumns.ID.value: annual_plan_id})
            .returning(AnnualPlanColumns.ID.value)
            .execute()
        )

        return builder


async def remove_annual_plan_partially(
        connection: AsyncConnection,
        annual_plan_id: str
):
    with exception_response():
        __annual_plan__ = RemoveAnnualPlanPartially(
            status=AnnualPlanStatus.DELETED
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ANNUAL_PLANS.value)
            .values(__annual_plan__)
            .check_exists({AnnualPlanColumns.ID.value: annual_plan_id})
            .where({AnnualPlanColumns.ID.value: annual_plan_id})
            .returning(AnnualPlanColumns.ID.value)
            .execute()
        )

        return builder