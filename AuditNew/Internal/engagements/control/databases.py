from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.control.schemas import *

def add_new_control(connection: Connection, control: Control, engagement_id: int):
    pass

def edit_control(connection: Connection, control: Control, control_id: int):
    pass

def remove_control(connection: Connection, control_id: int):
    pass