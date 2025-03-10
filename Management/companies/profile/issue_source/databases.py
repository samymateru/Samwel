from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.issue_source.schemas import *

def new_issue_source(connection: Connection, issue_source: IssueSource, company_id: int):
    pass

def delete_issue_source(connection: Connection, issue_source_id: int):
    pass

def edit_issue_source(connection: Connection, issue_source: IssueSource, issue_source_id: int):
    pass

def get_company_issue_source(connection: Connection, company_id: int):
    pass

def get_issue_source(connection: Connection, issue_source_id):
    pass