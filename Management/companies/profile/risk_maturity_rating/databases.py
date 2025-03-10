from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.risk_maturity_rating.schemas import *

def new_risk_maturity_rating(connection: Connection, maturity_rating: RiskMaturityRating, company_id: int):
    pass

def delete_risk_maturity_rating(connection: Connection, maturity_rating_id: int):
    pass

def edit_risk_maturity_rating(connection: Connection, maturity_rating: RiskMaturityRating, maturity_rating_id: int):
    pass

def get_company_risk_maturity_rating(connection: Connection, company_id: int):
    pass

def get_risk_maturity_rating(connection: Connection, maturity_rating_id):
    pass