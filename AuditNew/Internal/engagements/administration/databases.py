from typing import Dict, List
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.administration.schemas import *
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.schemas import UpdateEngagement, NewEngagement
import json

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
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                profile.audit_background,
                profile.audit_objectives,
                profile.key_legislations,
                profile.relevant_systems,
                profile.key_changes,
                profile.reliance,
                profile.scope_exclusion,
                profile.core_risk,
                profile.estimated_dates
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement profile")


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

def delete_profile(connection: Connection, engagement_id: int):
    query: str = """
                    DELETE FROM public.profile WHERE engagement = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (engagement_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement profile {e}")