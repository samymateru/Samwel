from typing import Dict, List
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.administration.schemas import *
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.schemas import UpdateEngagement, NewEngagement
import json

def add_engagement_profile(connection: Connection, profile: EngagementProfile, id: int):
    pass

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