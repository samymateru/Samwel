from psycopg import AsyncConnection
from core.tables import Tables
from schemas.attachement_schemas import ReadAttachment
from schemas.follow_up_schemas import CreateFollowUp, FollowUpStatus, FollowUpColumns, UpdateFollowUp, \
    ReviewFollowUp, DisApproveFollowUp, CompleteFollowUp, CreateFollowUpTest, NewFollowUpTest, FollowUpTestColumns, \
    UpdateFollowUpTest, FollowUpEngagements, FollowUpIssues, CreateFollowUpEngagement, CreateFollowUpIssue, \
    ReadFollowUpData, BaseFollowUpData
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def add_new_follow_up(
        connection: AsyncConnection,
        follow_up: CreateFollowUp,
):
    with exception_response():
        builder =  await (
            InsertQueryBuilder(connection=connection)
            .into_table("follow_up")
            .values(follow_up)
            .returning(FollowUpColumns.FOLLOW_UP_ID.value, FollowUpColumns.NAME.value)
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
        follow_up_id: str
):
    with exception_response():
        __follow_up__ = CompleteFollowUp(
            status=FollowUpStatus.REVIEWED,
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP.value)
            .values(__follow_up__)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({
                FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id,
                FollowUpColumns.STATUS.value: FollowUpStatus.PREPARED,
            })
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder


async def reset_follow_up_status_to_draft_model(
        connection: AsyncConnection,
        follow_up_id: str
):
    with exception_response():
        __follow_up__ = CompleteFollowUp(
            status=FollowUpStatus.DRAFT,
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



async def mark_follow_up_prepared_model(
        connection: AsyncConnection,
        follow_up_id: str
):
    with exception_response():
        __follow_up__ = CompleteFollowUp(
            status=FollowUpStatus.PREPARED,
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP.value)
            .values(__follow_up__)
            .check_exists({FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id})
            .where({
                FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id,
                FollowUpColumns.STATUS.value: FollowUpStatus.DRAFT
            })
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
            .where({
                FollowUpColumns.FOLLOW_UP_ID.value: follow_up_id,
                FollowUpColumns.STATUS.value: FollowUpStatus.REVIEWED,
            })
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )

        return builder



async def get_follow_up_test_model(
        connection: AsyncConnection,
        follow_up_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.FOLLOW_UP_TESTS.value)
            .where(FollowUpTestColumns.FOLLOW_UP_ID.value,  follow_up_id)
            .fetch_all()
        )

        return builder



async def add_follow_up_test_model(
        connection: AsyncConnection,
        follow_up_id: str,
        test: NewFollowUpTest
):
    with exception_response():
        __test__ = CreateFollowUpTest(
            test_id=get_unique_key(),
            follow_up_id=follow_up_id,
            name=test.name,
            description=test.description,
            outcome=test.outcome,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP_TESTS.value)
            .values(__test__)
            .check_exists({FollowUpTestColumns.NAME.value: test.name})
            .check_exists({FollowUpTestColumns.DESCRIPTION.value: test.description})
            .check_exists({FollowUpTestColumns.OUTCOME.value: test.outcome})
            .returning(FollowUpTestColumns.TEST_ID.value)
            .execute()
        )

        return builder



async def delete_follow_up_test_model(
        connection: AsyncConnection,
        test_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.FOLLOW_UP_TESTS.value)
            .check_exists({FollowUpTestColumns.TEST_ID.value: test_id})
            .where({FollowUpTestColumns.TEST_ID.value: test_id})
            .returning(FollowUpTestColumns.TEST_ID.value)
            .execute()
        )

        return builder



async def update_follow_up_test_model(
        connection: AsyncConnection,
        test_id: str,
        test: UpdateFollowUpTest
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_UP_TESTS.value)
            .values(test)
            .check_exists({FollowUpTestColumns.TEST_ID.value: test_id})
            .where({FollowUpTestColumns.TEST_ID.value: test_id})
            .returning(FollowUpTestColumns.TEST_ID.value)
            .execute()
        )

        return builder



async def attach_engagements_to_follow_up(
    connection: AsyncConnection,
    engagement_id: str,
    follow_up_id: str

):
    with exception_response():
        __follow_up_engagement__ = CreateFollowUpEngagement(
            engagement_id=engagement_id,
            follow_up_id=follow_up_id,
            follow_up_engagement_id=get_unique_key(),
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_ENGAGEMENTS.value)
            .values(__follow_up_engagement__)
            .check_exists({FollowUpEngagements.ENGAGEMENT_ID.value: engagement_id})
            .check_exists({FollowUpEngagements.FOLLOW_UP_ID.value: follow_up_id})
            .throw_error_on_exists(False)
            .returning(FollowUpEngagements.FOLLOW_UP_ENGAGEMENT_ID.value)
            .execute()
        )

        return builder



async def attach_issues_to_follow_up(
    connection: AsyncConnection,
    issue_id: str,
    follow_up_id: str

):
    with exception_response():

        __issue_follow_up__ = CreateFollowUpIssue(
            follow_up_issue_id=get_unique_key(),
            follow_up_id=follow_up_id,
            issue_id=issue_id,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.FOLLOW_ISSUES.value)
            .values(__issue_follow_up__)
            .check_exists({FollowUpIssues.ISSUE_ID.value: issue_id})
            .check_exists({FollowUpIssues.FOLLOW_UP_ID.value: follow_up_id})
            .throw_error_on_exists(False)
            .returning(FollowUpIssues.FOLLOW_UP_ISSUE_ID.value)
            .execute()
        )

        return builder



async def get_all_issues_on_follow_up(
    connection: AsyncConnection,
    follow_up_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.FOLLOW_ISSUES.value, alias="foll_iss")
            .join(
                "LEFT",
                Tables.ISSUES.value,
                "iss.id = foll_iss.issue_id",
                "iss",
                use_prefix=False
            )
            .where(FollowUpColumns.FOLLOW_UP_ID.value, follow_up_id)
            .fetch_all()
        )

        return builder



async def get_all_engagements_on_follow_up(
    connection: AsyncConnection,
    follow_up_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.FOLLOW_ENGAGEMENTS.value, alias="foll_eng")
            .join(
                "LEFT",
                Tables.ENGAGEMENTS.value,
                "eng.id = foll_eng.engagement_id",
                "eng",
                use_prefix=False
            )
            .where(FollowUpColumns.FOLLOW_UP_ID.value, follow_up_id)
            .fetch_all()
        )

        return builder




async def get_all_module_follow_up(
    connection: AsyncConnection,
    module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.FOLLOW_UP.value, alias="follow_up")
            .select(BaseFollowUpData)
            .join(
                "LEFT",
                Tables.ATTACHMENTS.value,
                "attachment.item_id = follow_up.follow_up_id",
                "attachment",
                use_prefix=True,
                model=ReadAttachment,
            )
            .where("follow_up."+FollowUpColumns.MODULE_ID.value, module_id)
            .select_joins()
            .fetch_all()
        )

        follow_ups = []

        for follow_up in builder:
            data = ReadFollowUpData(
                follow_up_id=follow_up.get("follow_up_id"),
                module_id=follow_up.get("module_id"),
                name=follow_up.get("name"),
                status=follow_up.get("status"),
                created_by=follow_up.get("created_by"),
                created_at=follow_up.get("created_at"),
                attachment=ReadAttachment(
                    attachment_id=follow_up.get("attachment_attachment_id"),
                    module_id=follow_up.get("attachment_attachment_id"),
                    item_id=follow_up.get("attachment_item_id"),
                    filename=follow_up.get("attachment_filename"),
                    category=follow_up.get("attachment_category"),
                    url=follow_up.get("attachment_url"),
                    size=follow_up.get("attachment_size"),
                    type=follow_up.get("attachment_type"),
                    created_at=follow_up.get("attachment_created_at")
                )
            )

            follow_ups.append(data)


        return follow_ups


async def set_issue_provisional_response(
    connection: AsyncConnection,
    module_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES.value)
        )