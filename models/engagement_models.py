from psycopg import AsyncConnection, sql
from core.tables import Tables
from schemas.engagement_schemas import NewEngagement, ArchiveEngagement, CompleteEngagement, EngagementStatus, \
    DeleteEngagementPartially, CreateEngagement, EngagementStage, EngagementColumns, AddOpinionRating, UpdateEngagement, \
    UpdateEngagement_
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def register_new_engagement(
        connection: AsyncConnection,
        engagement: NewEngagement,
        annual_plan_id: str,
        module_id: str,
):
    with exception_response():
        code = await generate_engagement_code(
            connection=connection,
            annual_plan_id=annual_plan_id,
            code=engagement.department.code
        )

        __engagement__ = CreateEngagement(
            id=get_unique_key(),
            plan_id=annual_plan_id,
            module_id=module_id,
            name=engagement.name,
            type=engagement.type,
            department=engagement.department,
            sub_departments=engagement.sub_departments,
            risk=engagement.risk.name,
            status=EngagementStatus.PENDING,
            stage=EngagementStage.PENDING,
            archived=False,
            start_date=engagement.start_date,
            end_date=engagement.end_date,
            created_at=datetime.now(),
            code=code,
            quarter="Q1",
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__engagement__)
            .check_exists({EngagementColumns.PLAN_ID.value: annual_plan_id})
            .check_exists({EngagementColumns.NAME.value: engagement.name})
            .returning(EngagementColumns.ID.value, EngagementColumns.CODE.value)
            .execute()
        )

        return builder



async def get_all_annual_plan_engagement(
        connection: AsyncConnection,
        annual_plan_id: str
):
    with exception_response():
        query = sql.SQL(
            """
            SELECT 
            eng.id,
            eng.plan_id,
            eng.module_id,
            eng.name,
            eng.type,
            eng.code,
            eng.status,
            eng.stage,
            eng.opinion_rating,
            eng.quarter,
            eng.sub_departments,
            eng.archived,
            eng.created_at,
            eng.department,
            eng.risk,
            eng.start_date,
            eng.end_date,
            COALESCE(
                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'id', stf.id,
                        'name', stf.name,
                        'email', stf.email,
                        'role', stf.role,
                        'start_date', stf.start_date,
                        'end_date', stf.end_date,
                        'tasks', stf.tasks
                    )
                ) FILTER (WHERE stf.id IS NOT NULL AND stf.role = 'Audit Lead'),
                '[]'::json
            ) AS leads
            FROM engagements eng
            LEFT JOIN staff stf 
                ON stf.engagement = eng.id
            WHERE eng.plan_id = %s AND eng.status NOT IN ('Deleted')
            GROUP BY eng.id, eng.plan_id, eng.name, eng.start_date, eng.end_date, eng.status;
            """)

        async with connection.cursor() as cursor:
            await cursor.execute(query, (annual_plan_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result



async def get_module_engagement_model(
        connection: AsyncConnection,
        status: EngagementStatus,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS.value)
            .where(EngagementColumns.MODULE_ID.value, module_id)
            .where(EngagementColumns.STATUS.value, status.value)
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


async def update_engagement_data(
        connection: AsyncConnection,
        engagement: UpdateEngagement_,
        engagement_id: str
):
    with exception_response():
        __engagement__ = UpdateEngagement(
            name=engagement.name,
            type=engagement.type,
            risk=engagement.risk.name,
            department=engagement.department,
            sub_departments=engagement.sub_departments,
            start_date=engagement.start_date,
            end_date=engagement.end_date
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__engagement__)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder


async def generate_engagement_code(
        connection: AsyncConnection,
        code: str,
        annual_plan_id: str
):
    with exception_response():
        code_list = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS)
            .select_fields("code")
            .where(EngagementColumns.PLAN_ID.value, annual_plan_id)
            .fetch_all()
        )
        max_ = 0

        codes = [item['code'] for item in code_list]
        for data in codes:
            code_ = data.split("-")
            if code == code_[0]:
                if int(code_[1]) >= max_:
                    max_ = int(code_[1])
        return code + "-" + str(max_ + 1).zfill(3) + "-" + str(datetime.now().year)


