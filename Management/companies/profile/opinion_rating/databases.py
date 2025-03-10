from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.opinion_rating.schemas import *

def new_opinion_rating(connection: Connection, opinion_rating: OpinionRating, company_id: int):
    pass

def delete_opinion_rating(connection: Connection, opinion_rating_id: int):
    pass

def edit_opinion_rating(connection: Connection, opinion_rating: OpinionRating, opinion_rating_id: int):
    pass

def get_company_opinion_rating(connection: Connection, company_id: int):
    pass

def get_opinion_rating(connection: Connection, opinion_rating_id):
    pass