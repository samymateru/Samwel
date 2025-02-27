from psycopg2.extensions import connection as Connection

def risk_rating(connection: Connection, company: int):
    values = [
        (company, "Very High Risk", 4),
        (company, "High Risk", 3),
        (company, "Medium Risk", 2),
        (company, "Low Risk", 1),
    ]
    query: str = f"""
                 INSERT INTO public.risk_rating (company, name, magnitude)
                 VALUES(%s, %s, %s)
                 """
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def issue_finding_source(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.issue_finding_source (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Internal Audit", company),
        ("External Audit", company),
        ("Self Disclosed", company),
        ("Regulator Audit/Examination", company),
        ("Other Assurance Reviews", company)
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def control_effectiveness_rating(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.control_effectiveness_rating (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Effective", company),
        ("Partially Effective", company),
        ("Ineffective", company),
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def control_weakness_rating(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.control_weakness_rating (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Acceptable", company),
        ("Improvement Required", company),
        ("Significant Improvement Required", company),
        ("Unacceptable", company)
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def audit_opinion_rating(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.audit_opinion_rating (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("High Assurance", company),
        ("Reasonable Assurance", company),
        ("Limited Assurance", company),
        ("No Assurance", company)
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def risk_maturity_rating(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.maturity_rating (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Risk naive", company),
        ("Risk aware", company),
        ("Risk defined", company),
        ("Risk managed", company),
        ("Risk managed", company)
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()


def issue_implementation_status(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.issue_implementation_status (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Pending", company),
        ("In progress", company),
        ("Implemented", company),
        ("Closed but not verified by (LOD 2)", company),
        ("Closed and  verified by (LOD 2)", company),
        ("Closed-Risk tolerated by management", company),
        ("Closed-No Longer Applicable", company),
        ("Closed not verified by Audit", company),
        ("Closed and verified by Audit", company)
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def control_type(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.control_type (name, company)
                 VALUES (%s, %s)
                 """
    values = [
        ("Preventive control", company),
        ("Detective control", company),
        ("Corrective control", company),
        ("Compensating control", company),
    ]
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

def roles(connection: Connection, company: int):
    query: str = """
                 INSERT INTO public.roles (roles, company)
                 VALUES (%s, %s)
                 """
    values = [
	{
	  "name": "Owner",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Administrator",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Auditor",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Chief Executive Officer",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Chief Financial Officer",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Chief Information Officer",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Chief Operations Officer",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Chief Information Security Officer",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Head of Internal Audit",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Senior Audit Manager",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	},
	{
	  "name": "Risk Manager",
        "categories": {
            "module": ["view", "edit", "delete", "assign", "approve"],
            "user": ["view", "edit", "delete", "assign", "approve"],
            "annual_plan": ["view", "edit", "delete", "assign", "approve"],
            "engagement": ["view", "edit", "delete", "assign", "approve"],
            "store": ["view", "edit", "delete", "assign", "approve"],
            "role": ["view", "edit", "delete", "assign", "approve"]
        }
	}
   ]

    with connection.cursor() as cursor:
        cursor.execute(query, (values, company))
    connection.commit()

def business_process(connection: Connection, company: int):
    data = [
        {"name": "process1", "code": "CQ", "sub":["sub1", "sub2"]},
        {"name": "process1", "code": "CQ", "sub": ["sub1", "sub2"]}
    ]
    with connection.cursor() as cursor:
        process_ids = {}

        # 1️⃣ Insert Business Processes & Get Their IDs
        for process in data:
            cursor.execute(
                "INSERT INTO business_process (process_name, code, company) VALUES (%s, %s, %s) RETURNING id;",
                (process["name"], process["code"], company)
            )
            process_id = cursor.fetchone()[0]
            process_ids[process["name"]] = process_id  # Store process ID

        # 2️⃣ Insert Business Subprocesses (Batch Insert)
        subprocess_values = []
        for process in data:
            process_id = process_ids[process["name"]]
            for sub in process["sub"]:
                subprocess_values.append((sub, process_id))

        # Execute batch insert
        cursor.executemany(
            "INSERT INTO business_sub_process (name, business_process) VALUES (%s, %s);",
            subprocess_values
        )

        connection.commit()




