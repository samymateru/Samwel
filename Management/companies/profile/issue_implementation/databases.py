from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.issue_implementation.schemas import *

def new_issue_implementation(connection: Connection, issue_implementation: IssueImplementation, company_id: int):
    pass

def delete_issue_implementation(connection: Connection, issue_implementation_id: int):
    pass

def edit_issue_implementation(connection: Connection, issue_implementation: IssueImplementation, issue_implementation_id: int):
    pass

def get_company_issue_implementation(connection: Connection, company_id: int):
    pass

def get_issue_implementation(connection: Connection, issue_implementation_id):
    pass