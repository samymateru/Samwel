from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.risk_rating.schemas import *

def new_risk_rating(connection: Connection, risk_rating: RiskRating, company_id: int):
    pass

def delete_risk_rating(connection: Connection, risk_rating_id: int):
    pass

def edit_risk_rating(connection: Connection, risk_rating: RiskRating, risk_rating_id: int):
    pass

def get_company_risk_rating(connection: Connection, company_id: int):
    pass

def get_risk_rating(connection: Connection, risk_rating_id):
    pass