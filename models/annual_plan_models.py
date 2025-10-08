from psycopg import AsyncConnection
from core.tables import Tables
from models.module_models import get_data_reference_in_module, increment_module_reference
from schemas.annual_plan_schemas import NewAnnualPlan, CreateAnnualPlan, AnnualPlanStatus, AnnualPlanColumns, \
    UpdateAnnualPlan, RemoveAnnualPlanPartially, ReadAnnualPlan, AnnualPlan
from schemas.attachement_schemas import ReadAttachment
from schemas.module_schemas import ModuleDataReference, IncrementPlanReferences
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from services.logging.logger import global_logger
from utils import exception_response, get_unique_key
from datetime import datetime


async def register_new_annual_plan(
        connection: AsyncConnection,
        annual_plan: NewAnnualPlan,
        module_id: str,
        user_id: str
):
    with exception_response():
        reference = await generate_plan_reference(
            connection=connection,
            module_id=module_id,
            year=annual_plan.year
        )

        __annual_plan__ = CreateAnnualPlan(
            id=get_unique_key(),
            module=module_id,
            reference=reference or "P-0001",
            name=annual_plan.name,
            year=annual_plan.year,
            start=annual_plan.start,
            end=annual_plan.end,
            status=AnnualPlanStatus.PENDING,
            creator=user_id,
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
            .from_table(Tables.ANNUAL_PLANS.value, alias="pln")
            .select(AnnualPlan)
            .join(
                "LEFT",
                Tables.ATTACHMENTS.value,
                "attachment.item_id = pln.id",
                "attachment",
                use_prefix=True,
                model=ReadAttachment,
            )
            .select_joins()
            .where(AnnualPlanColumns.MODULE.value, module_id)
            .where_raw("pln.status IN ('Pending')")
            .fetch_all()
        )

        plans = []

        for plan in builder:
            data = ReadAnnualPlan(
                id=plan.get("id"),
                module=plan.get("module"),
                reference=plan.get("reference"),
                name=plan.get("name"),
                year=plan.get("year"),
                start=plan.get("start"),
                end=plan.get("end"),
                status=plan.get("status"),
                creator=plan.get("creator"),
                created_at=plan.get("created_at"),
                attachment=ReadAttachment(
                    attachment_id=plan.get("attachment_attachment_id"),
                    module_id=plan.get("attachment_attachment_id"),
                    item_id=plan.get("attachment_item_id"),
                    filename=plan.get("attachment_filename"),
                    category=plan.get("attachment_category"),
                    url=plan.get("attachment_url"),
                    size=plan.get("attachment_size"),
                    type=plan.get("attachment_type"),
                    created_at=plan.get("attachment_created_at")
                )

            )

            plans.append(data)

        return plans



async def get_annual_plan_details(
        connection: AsyncConnection,
        annual_plan_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ANNUAL_PLANS.value)
            .where(AnnualPlanColumns.ID.value, annual_plan_id)
            .where_raw("status IN ('Pending')")
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
            status=AnnualPlanStatus.DELETED,
            name=get_unique_key()
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



async def generate_plan_reference(
    connection: AsyncConnection,
    module_id: str,
    year: str
):
    with exception_response():
        count = await get_data_reference_in_module(
            connection=connection,
            module_id=module_id,
            sections=ModuleDataReference.PLAN_REFERENCE
        )


        if count is None:
            count = 0
            global_logger.exception(
                "Error While Fetching Plan Reference"
            )


        value = IncrementPlanReferences(
            plan_reference=count + 1
        )

        results = await increment_module_reference(
            connection=connection,
            module_id=module_id,
            value=value
        )

        if results is None:
            global_logger.exception("Error While Incrementing Plan Reference")


        return f"P{count + 1:04d}-{year}"