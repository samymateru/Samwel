from typing import Dict

from fastapi import HTTPException
from psycopg import AsyncConnection, sql
from core.tables import Tables
from models.engagement_staff_models import create_new_engagement_staff_model
from models.notification_models import add_notification_to_user_model
from models.recent_activity_models import add_new_recent_activity
from schemas.annual_plan_schemas import ReadAnnualPlan
from schemas.engagement_schemas import NewEngagement, ArchiveEngagement, CompleteEngagement, EngagementStatus, \
    DeleteEngagementPartially, CreateEngagement, EngagementStage, EngagementColumns, AddOpinionRating, UpdateEngagement, \
    UpdateEngagement_, Engagement, EngagementRiskMaturityRating, UpdateEngagementRiskMaturityRating, \
    UpdateRiskMaturityRatingLowerPart
from schemas.engagement_staff_schemas import NewEngagementStaff, NewStage
from schemas.notification_schemas import CreateNotifications, NotificationsStatus
from schemas.recent_activities_schemas import RecentActivities, RecentActivityCategory
from schemas.user_schemas import UserColumns
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from services.logging.logger import global_logger
from utils import exception_response, get_unique_key
from datetime import datetime


async def register_new_engagement(
        connection: AsyncConnection,
        engagement: NewEngagement,
        annual_plan_id: str,
        module_id: str
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
            quarter=engagement.quarter,
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(__engagement__)
            .check_exists({EngagementColumns.PLAN_ID.value: annual_plan_id})
            .check_exists({EngagementColumns.NAME.value: engagement.name})
            .returning(EngagementColumns.ID.value, EngagementColumns.CODE.value, EngagementColumns.NAME)
            .execute()
        )

        return builder



async def get_all_annual_plan_engagement(
        connection: AsyncConnection,
        annual_plan_id: str,
        user_id: str
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
                        'role', stf.role
                    )
                ) FILTER (WHERE stf.id IS NOT NULL AND stf.role = 'Audit Lead'),
                '[]'::json
            ) AS leads
            FROM engagements eng
            LEFT JOIN staff stf ON stf.engagement = eng.id
            WHERE eng.plan_id = %s AND eng.status NOT IN ('Deleted') AND stf.user_id = %s
            GROUP BY eng.id, eng.plan_id, eng.name, eng.status;
            """)

        async with connection.cursor() as cursor:
            await cursor.execute(query, (annual_plan_id, user_id))
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



async def get_single_engagement_with_plan_details(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENTS.value, alias="eng")
            .select(Engagement)
            .join(
                "LEFT",
                Tables.ANNUAL_PLANS.value,
                "pln.id = eng.plan_id",
                "pln",
                use_prefix=True,
                model=ReadAnnualPlan
            )
            .select_joins()
            .where("eng."+EngagementColumns.ID.value, engagement_id)
            .fetch_one()
        )

        return builder



async def archive_annual_plan_engagement(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        __archive__ =  ArchiveEngagement(
            archived=True,
            status=EngagementStatus.ARCHIVED.value
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
            status=EngagementStatus.DELETED,
            name=get_unique_key(),
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



async def update_risk_maturity_rating_table_model(
        connection: AsyncConnection,
        engagement: EngagementRiskMaturityRating,
        engagement_id: str
):
    with exception_response():
        __engagement__ = UpdateEngagementRiskMaturityRating(
            risk_maturity_rating=engagement.model_dump()
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




async def update_risk_maturity_rating_lower_section_model(
        connection: AsyncConnection,
        engagement: UpdateRiskMaturityRatingLowerPart,
        engagement_id: str,
):
    with exception_response():

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENTS.value)
            .values(engagement)
            .check_exists({EngagementColumns.ID.value: engagement_id})
            .where({EngagementColumns.ID.value: engagement_id})
            .returning(EngagementColumns.ID.value)
            .execute()
        )

        return builder



async def adding_engagement_staff_model(
        head_of_audit: Dict,
        engagement_id: str,
        engagement: NewEngagement,
        module_id: str
):
    pool = await AsyncDBPoolSingleton.get_instance().get_pool()

    with exception_response():
        async with pool.connection() as connection:
            entity_user_data = await (
                ReadBuilder(connection=connection)
                .from_table(Tables.USERS.value)
                .where(UserColumns.ID.value, head_of_audit.get("user_id"))
                .fetch_one()
            )


            if entity_user_data is None:
                global_logger.exception("No Head Of Audit Found, Cant Create Engagement")
                raise HTTPException(status_code=400, detail="No Head Of Audit Found, Cant Create Engagement")


            staff = NewEngagementStaff(
                name=entity_user_data.get("name"),
                role=head_of_audit.get("role"),
                email=entity_user_data.get("email"),
                user_id=head_of_audit.get("user_id") or "",
                role_id=head_of_audit.get("role_id") or "",
                planning=NewStage(
                    hours=10,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                ),
                fieldwork=NewStage(
                    hours=10,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                ),
                reporting=NewStage(
                    hours=10,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                ),
                finalization=NewStage(
                    hours=10,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                )
            )


            await create_new_engagement_staff_model(
                connection=connection,
                staff=staff,
                engagement_id=engagement_id
            )


            await add_notification_to_user_model(
                connection=connection,
                notification=CreateNotifications(
                    id=get_unique_key(),
                    title="Engagement invitation",
                    user_id=entity_user_data.get("id"),
                    message=f"Your have been invited to engagement {engagement.name} as Head Of Audit",
                    status=NotificationsStatus.NEW,
                    created_at=datetime.now()
                )
            )


            for lead in engagement.leads:
                staff = NewEngagementStaff(
                    name=lead.name,
                    user_id=lead.id,
                    role="Audit Lead",
                    role_id="",
                    email=lead.email,
                    planning=NewStage(
                        hours=10,
                        start_date=datetime.now(),
                        end_date=datetime.now()
                    ),
                    fieldwork = NewStage(
                        hours=10,
                        start_date=datetime.now(),
                        end_date=datetime.now()
                    ),
                    reporting=NewStage(
                        hours=10,
                        start_date=datetime.now(),
                        end_date=datetime.now()
                    ),
                    finalization=NewStage(
                        hours=10,
                        start_date=datetime.now(),
                        end_date=datetime.now()
                    )
                )

                await create_new_engagement_staff_model(
                    connection=connection,
                    staff=staff,
                    engagement_id=engagement_id
                )



                await add_notification_to_user_model(
                    connection=connection,
                    notification=CreateNotifications(
                        id=get_unique_key(),
                        title="Engagement invitation",
                        user_id=lead.id,
                        message=f"Your have been invited to engagement {engagement.name} as Engagement lead",
                        status=NotificationsStatus.NEW,
                        created_at=datetime.now()
                    )
                )


            await add_new_recent_activity(
                connection=connection,
                recent_activity=RecentActivities(
                    activity_id=get_unique_key(),
                    module_id=module_id,
                    name=engagement.name,
                    description="New Engagement Created",
                    category=RecentActivityCategory.ENGAGEMENT_CREATED,
                    created_by="",
                    created_at=datetime.now()
                )
            )


async def update_engagement_to_in_progress(
        engagement_id: str
):
    pool = await AsyncDBPoolSingleton.get_instance().get_pool()
    with exception_response():
        async with pool.connection() as connection:
            data = await (
                UpdateQueryBuilder(connection=connection)
                .into_table(Tables.ENGAGEMENTS.value)
                .values({"status": EngagementStatus.ONGOING.value})
                .where({EngagementColumns.ID.value: engagement_id})
                .check_exists({EngagementColumns.ID.value: engagement_id})
                .returning(EngagementColumns.ID.value)
                .execute()
            )

            if data is None:
                global_logger.exception("Fail To Update Engagement To In Progress")



async def get_engagement_stage(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        query_procedures = sql.SQL(
            """
            WITH finalization_summary AS (
            SELECT
            COUNT(*) AS total_finalization_procedures,
            jsonb_build_object(
                'pending', COUNT(*) FILTER (WHERE fp.prepared_by IS NULL AND fp.reviewed_by IS NULL),
                'in_progress', COUNT(*) FILTER (WHERE fp.prepared_by IS NOT NULL AND fp.reviewed_by IS NULL),
                'completed', COUNT(*) FILTER (WHERE fp.prepared_by IS NOT NULL AND fp.reviewed_by IS NOT NULL)
            ) AS finalization_status_summary
            FROM finalization_procedure fp
            JOIN engagements e ON fp.engagement = e.id
            WHERE e.id = {engagement_id}
            ),
            reporting_summary AS (
            SELECT
            COUNT(*) AS total_reporting_procedures,
            jsonb_build_object(
                'pending', COUNT(*) FILTER (WHERE rp.prepared_by IS NULL AND rp.reviewed_by IS NULL),
                'in_progress', COUNT(*) FILTER (WHERE rp.prepared_by IS NOT NULL AND rp.reviewed_by IS NULL),
                'completed', COUNT(*) FILTER (WHERE rp.prepared_by IS NOT NULL AND rp.reviewed_by IS NOT NULL)
            ) AS report_status_summary
            FROM reporting_procedure rp
            JOIN engagements e ON rp.engagement = e.id
            WHERE e.id = {engagement_id}
            ),
            profile_summary AS (
            SELECT
            COUNT(*) AS total_profile_summary,
            jsonb_build_object(
                'pending', COUNT(*) FILTER (WHERE pr.prepared_by IS NULL AND pr.reviewed_by IS NULL),
                'in_progress', COUNT(*) FILTER (WHERE pr.prepared_by IS NOT NULL AND pr.reviewed_by IS NULL),
                'completed', COUNT(*) FILTER (WHERE pr.prepared_by IS NOT NULL AND pr.reviewed_by IS NOT NULL)
            ) AS profile_status_summary
            FROM profile pr
            JOIN engagements e ON pr.engagement = e.id
            WHERE e.id = {engagement_id}
            ),
            planning_summary AS (
            SELECT
            COUNT(*) AS total_planning_procedures,
            jsonb_build_object(
                'pending', COUNT(*) FILTER (WHERE tmp.prepared_by IS NULL AND tmp.reviewed_by IS NULL),
                'in_progress', COUNT(*) FILTER (WHERE tmp.prepared_by IS NOT NULL AND tmp.reviewed_by IS NULL),
                'completed', COUNT(*) FILTER (WHERE tmp.prepared_by IS NOT NULL AND tmp.reviewed_by IS NOT NULL)
            ) AS planning_status_summary
            FROM std_template tmp
            JOIN engagements e ON tmp.engagement = e.id
            WHERE e.id = {engagement_id}
            ),
            work_program_summary AS (
            SELECT
            COUNT(*) AS total_work_program_procedures,
            jsonb_build_object(
                'pending', COUNT(*) FILTER (WHERE sp.prepared_by IS NULL AND sp.reviewed_by IS NULL),
                'in_progress', COUNT(*) FILTER (WHERE sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NULL),
                'completed', COUNT(*) FILTER (WHERE sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NOT NULL)
            ) AS work_program_procedure_status_summary
            FROM main_program mp
            JOIN engagements e ON mp.engagement = e.id
            JOIN sub_program sp ON sp.program = mp.id
            WHERE e.id = {engagement_id}
            )
            SELECT
            fs.total_finalization_procedures,
            fs.finalization_status_summary,
            rs.total_reporting_procedures,
            rs.report_status_summary,
            ps.total_planning_procedures,
            ps.planning_status_summary,
            pr.profile_status_summary,
            pr.total_profile_summary,
            wp.total_work_program_procedures,
            wp.work_program_procedure_status_summary
            FROM 
            finalization_summary fs, 
            reporting_summary rs, 
            planning_summary ps,
            profile_summary pr,
            work_program_summary wp;
            """
        ).format(engagement_id=sql.Literal(engagement_id))


        async with connection.cursor() as cursor:
            await cursor.execute(query_procedures)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            procedure_data = [dict(zip(column_names, row_)) for row_ in rows]
            if procedure_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No data found")
            return procedure_data