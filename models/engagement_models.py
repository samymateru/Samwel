from psycopg import AsyncConnection
from core.tables import Tables
from schemas.engagement_schemas import NewEngagement, ArchiveEngagement, CompleteEngagement, EngagementStatus, \
    DeleteEngagementPartially, CreateEngagement, EngagementStage, EngagementColumns, AddOpinionRating
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def register_new_engagement(
        connection: AsyncConnection,
        engagement: NewEngagement,
        annual_plan_id: str,
        module_id: str
):
    with exception_response():
        __engagement__ = CreateEngagement(
            id=get_unique_key(),
            plan_id=annual_plan_id,
            module_id=module_id,
            name=engagement.name,
            type=engagement.type,
            department=engagement.department,
            sub_departments=engagement.sub_departments,
            risk=engagement.risk,
            status=EngagementStatus.PENDING,
            stage=EngagementStage.PENDING,
            start_date=engagement.start_date,
            end_date=engagement.end_date,
            created_at=datetime.now(),
            code="",
            quarter="Q1",
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__engagement__)
            .check_exists({EngagementColumns.PLAN_ID.value: annual_plan_id})
            .check_exists({EngagementColumns.NAME.value: engagement.name})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder

async def get_all_annual_plan_engagement(
        connection: AsyncConnection,
        annual_plan_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS.value)
            .where(EngagementColumns.PLAN_ID.value, annual_plan_id)
            .fetch_all()
        )

        return builder


async def get_all_module_engagement(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS.value)
            .where(EngagementColumns.MODULE_ID.value, module_id)
            .fetch_all()
        )

        return builder


async def get_single_engagement_details(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS.value)
            .where(EngagementColumns.ID.value, engagement_id)
            .fetch_one()
        )

        return builder


async def archive_annual_plan_engagement(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        __archive__ =  ArchiveEngagement(
            archived=True
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__archive__)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder


async def complete_annual_plan_engagement(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        __complete__ =  CompleteEngagement(
            status=EngagementStatus.COMPLETED
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__complete__)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder


async def remove_engagement_partially(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        __remove__ =  DeleteEngagementPartially(
            status=EngagementStatus.DELETED
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__remove__)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder

async def update_engagement_opinion_rating(
        connection: AsyncConnection,
        opinion_rating: AddOpinionRating,
        engagement_id: str
):
    with exception_response():

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(opinion_rating)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder
