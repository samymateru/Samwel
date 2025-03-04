from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.administration.schemas import *
from psycopg2.extensions import cursor as Cursor


def add_engagement_profile(connection: Connection, profile: EngagementProfile, engagement_id: int):
    query: str = """
                   INSERT INTO public.profile (
                        engagement,
                        audit_background,
                        audit_objectives,
                        key_legislations,
                        relevant_systems,
                        key_changes,
                        reliance,
                        scope_exclusion,
                        core_risk,
                        estimated_dates
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                profile.audit_background.model_dump_json(),
                profile.audit_objectives.model_dump_json(),
                profile.key_legislations.model_dump_json(),
                profile.relevant_systems.model_dump_json(),
                profile.key_changes.model_dump_json(),
                profile.reliance.model_dump_json(),
                profile.scope_exclusion.model_dump_json(),
                profile.core_risk,
                profile.estimated_dates.model_dump_json()
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement profile {e}")

def add_engagement_policies(connection: Connection, policy: Policy, engagement_id: int):
    query: str = """
                   INSERT INTO public.policies (
                        engagement,
                        name,
                        version,
                        key_areas,
                        attachment
                   ) VALUES(%s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                policy.name,
                policy.version,
                policy.key_areas,
                policy.attachment
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement policy {e}")

def add_engagement_process(connection: Connection, process: EngagementProcess, engagement_id: int):
    query: str = """
                   INSERT INTO public.engagement_process (
                        engagement,
                        process,
                        sub_process,
                        description,
                        business_unit
                   ) VALUES(%s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                process.process,
                process.sub_process,
                process.description,
                process.business_unit
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement process {e}")

def add_engagement_regulations(connection: Connection, regulation: Regulations, engagement_id: int):
    query: str = """
                   INSERT INTO public.regulations (
                        engagement,
                        name,
                        issue_date,
                        key_areas,
                        attachment
                   ) VALUES(%s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                regulation.name,
                regulation.issue_date,
                regulation.key_areas,
                regulation.attachment
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement regulation {e}")

def add_engagement_staff(connection: Connection, staff: Staff, engagement_id: int):
    query: str = """
                   INSERT INTO public.staff (
                        engagement,
                        name,
                        role,
                        start_date,
                        end_date,
                        tasks
                   ) VALUES(%s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                staff.name,
                staff.role.model_dump_json(),
                staff.start_date,
                staff.end_date,
                staff.tasks
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement staff {e}")

def get_engagement_profile(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                    SELECT * from public.profile 
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement profile {e}")


def get_engagement_policies(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                    SELECT * from public.policies
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement policies {e}")

def get_engagement_process(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                    SELECT * from public.engagement_process
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement processes {e}")

def get_engagement_regulations(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                    SELECT * from public.regulations
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement regulations {e}")


def get_engagement_staff(connection: Connection, column: str = None, value: int | str = None):
    query: str = """
                    SELECT * from public.staff
                 """
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement staffing {e}")


def remove_profile(connection: Connection, profile_id: int):
    query: str = """
                    DELETE FROM public.profile WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (profile_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement profile {e}")


def remove_policy(connection: Connection, policy_id: int):
    query: str = "DELETE FROM public.policies WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (policy_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing policy {e}")


def remove_staff(connection: Connection, staff_id: int):
    query: str = "DELETE FROM public.staff WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (staff_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing staff {e}")

def remove_regulation(connection: Connection, regulation_id: int):
    query: str = "DELETE FROM public.regulations WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (regulation_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing regulation {e}")

