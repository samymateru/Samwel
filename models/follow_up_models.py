from typing import List
from psycopg import AsyncConnection
from core.tables import Tables
from schemas.follow_up_schemas import CreateFollowUp, FollowUpStatus, FollowUpColumns, UpdateFollowUp, \
    ReviewFollowUp, DisApproveFollowUp, CompleteFollowUp
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response


async def add_new_follow_up(
        connection: AsyncConnection,
        follow_up: CreateFollowUp,
):
    with exception_response():
        builder =  await (
            InsertQueryBuilder(connection=connection)
            .into_table("follow_up")
            .values(follow_up)
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )
        return builder


async def update_follow_up_details_model(
        connection: AsyncConnection,
        follow_up: UpdateFollowUp,
        follow_up_id: str
):
    with exception_response():
        builder =  await (
            UpdateQueryBuilder(connection=connection)
            .into_table("follow_up")
            .values(follow_up)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )
        return builder


async def remove_follow_up_data_model(
        connection: AsyncConnection,
        follow_up_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.FOLLOW_UP.value)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder


async def approve_follow_up_data_model(
        connection: AsyncConnection,
        follow_up_id: str,
        reviewed_by: str
):
    with exception_response():
        __follow_up__ = ReviewFollowUp(
            reviewed_by=reviewed_by,
            status=FollowUpStatus.PREPARED,
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP.value)
            .values(__follow_up__)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder


async def reset_follow_up_status_to_draft_model(
        connection: AsyncConnection,
        follow_up_id: str
):
    with exception_response():
        __follow_up__ = DisApproveFollowUp(
            status=FollowUpStatus.DRAFT,
            reviewed_by=""
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP.value)
            .values(__follow_up__)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder


async def complete_follow_up_model(
        connection: AsyncConnection,
        follow_up_id: str
):
    with exception_response():
        __follow_up__ = CompleteFollowUp(
            status=FollowUpStatus.COMPLETED,
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP.value)
            .values(__follow_up__)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder



async def attach_engagements_to_follow_up(
    connection: AsyncConnection,
    engagement_ids: List[str]

):
    with exception_response():
        pass


async def attach_issues_to_follow_up(
    connection: AsyncConnection,
    issue_ids: List[str]

):
    with exception_response():
        pass