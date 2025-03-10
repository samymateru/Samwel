from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.control_weakness_rating.schemas import *

def new_control_weakness_rating(connection: Connection,control_weakness_rating: ControlWeaknessRating, company_id: int):
    pass

def delete_control_weakness_rating(connection: Connection, control_weakness_rating_id: int):
    pass

def edit_control_weakness_rating(connection: Connection, control_weakness_rating: ControlWeaknessRating, control_weakness_rating_id: int):
    pass

def get_company_control_weakness_rating(connection: Connection, company_id: int):
    pass

def get_control_weakness_rating(connection: Connection, control_weakness_rating_id):
    pass