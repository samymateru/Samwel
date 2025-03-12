import json
from fastapi import HTTPException
from psycopg import Cursor

from psycopg2.extensions import connection as Connection
from AuditNew.Internal.engagements.planning.databases import add_planning_procedure

def engagement_types(connection: Connection, company: int):
    values = [
        (company, "Internal Audit"),
        (company, "Compliance Audit"),
        (company, "Operational Audit"),
        (company, "IT Audit"),
        (company, "Forensic Audit"),
        (company, "Financial Audit"),
        (company, "Performance Audit"),
        (company, "Environmental Audit"),
        (company, "Tax Audit")
    ]
    query: str = f"""
                 INSERT INTO public.engagement_types (company, name)
                 VALUES(%s, %s)
                 """
    with connection.cursor() as cursor:
        cursor.executemany(query, values)
    connection.commit()

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
                 INSERT INTO public.opinion_rating (name, company)
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
                 INSERT INTO public.risk_maturity_rating (name, company)
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
                 INSERT INTO public.issue_implementation (name, company)
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
    values = [
        {
            "name": "Owner",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Admin",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Chief Executive Officer",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Chief Financial Officer",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Chief Information Officer",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Chief Operation Officer",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name":"Chief Information Security Officer",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Head of Audit",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Senior Audit Manager",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },
        {
            "name": "Risk Manager",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        }
   ]
    with connection.cursor() as cursor:
        role_values = [(json.dumps({"name": role["name"], "creator": role["creator"], "categories": role["categories"]}), company) for role in values]

        cursor.executemany(
            "INSERT INTO public.roles (roles, company) VALUES (%s::jsonb, %s);",
            role_values
        )
    connection.commit()

def business_process(connection: Connection, company: int):
    data = [
        {
            "name": "Finance",
            "code": "FN",
            "sub": [
                "Revenue management",
                "Payment management",
                "Tax compliance",
                "General ledger and financial reporting",
                "Cash management",
                "Accounts payable",
                "Accounts receivable",
                "Budgeting",
                "Fixed asset management"
            ]
        },
        {
            "name": "Credit / Lending",
            "code": "CR",
            "sub": [
                "Credit origination",
                "Loan disbursement",
                "Loan provisioning/Impairment",
                "Collaterals management",
                "Credit",
                "Loan recovery"
            ]
        },
        {
            "name": "Human Resources",
            "code": "HR",
            "sub": [
                "Recruitment and onboarding",
                "Payroll and employee benefits",
                "Training and development",
                "Promotion",
                "Performance Management",
                "Disciplinary management and employee relations",
                "Termination and Separation"
            ]
        },
        {
            "name": "Information Technology",
            "code": "IT",
            "sub": [
                "System development",
                "IT General Controls (ITGCs)",
                "IT security",
                "IT infrastructure and data security",
                "Software acquisition and licensing",
                "Backup",
                "Disaster recovery",
                "Business continuity"
            ]
        },
        {
            "name": "Business Development",
            "code": "BD",
            "sub": [
                "Business originations",
                "Customer relationship management (CRM)",
                "Pricing and promotions",
                "Commission",
                "Proposals and Bidding",
                "Delivery management"
            ]
        },
        {
            "name": "Compliance",
            "code": "CM",
            "sub": [
                "Regulatory compliance",
                "Licensing",
                "Anti-fraud process",
                "Data privacy and confidentiality"
            ]
        },
        {
            "name": "Operations",
            "code": "OP",
            "sub": [
                "Process design",
                "Inventory management and supply chain",
                "Production and manufacturing processes."
            ]
        },
        {
            "name": "Procurement",
            "code": "PR",
            "sub": [
                "Vendor selection and contract management",
                "Purchase order approvals and payments",
                "Fraud prevention and compliance",
                "Supply Chain Management"
            ]
        },
        {
            "name": "Risk Management",
            "code": "RM",
            "sub": [
                "Risk Assessment",
                "Key risk indicators",
                "Insurance and risk mitigation plans",
                "Incident responses",
                "Crisis management",
                "Environmental, social, and governance (ESG)"
            ]
        },
        {
            "name": "Customer Management",
            "code": "CU",
            "sub": [
                "Complaints management",
                "Customer satisfaction and retention programs",
                "Data privacy and service-level agreements (SLAs)"
            ]
        },
        {
            "name": "Deposit Management",
            "code": "DP",
            "sub": [
                "Customer onboarding",
                "Deposits pricing",
                "Deposit mix",
                "Product design"
            ]
        },
        {
            "name": "Banking Operations",
            "code": "BO",
            "sub": [
                "New clients take on",
                "Cheque process",
                "Bank transfers",
                "Fixed Deposits",
                "Product design"
            ]
        },
        {
            "name": "Branch Operations",
            "code": "BR",
            "sub": [
                "Branch security",
                "Deposits management",
                "Account opening",
                "KYC",
                "Branch credit",
                "Documentation management"
            ]
        },
        {
            "name": "Treasury Operations",
            "code": "TR",
            "sub": [
                "Forex transaction",
                "Global markets",
                "Assets and Liability Management (ALM)",
                "Liquidity management",
                "Sensitivity and stress testing",
                "Product design and pricing"
            ]
        }

    ]
    with connection.cursor() as cursor:
        process_ids = {}

        # 1️⃣ Insert Business Processes & Get Their IDs
        for process in data:
            cursor.execute(
                "INSERT INTO public.business_process (process_name, code, company) VALUES (%s, %s, %s) RETURNING id;",
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
            "INSERT INTO public.business_sub_process (name, business_process) VALUES (%s, %s);",
            subprocess_values
        )
        connection.commit()

def planning_procedures(connection: Connection, engagement: int):
    values = [
        {
            "title": "Pre-engagement meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Client notification",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Audit mobilization meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Allocation of staff",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "id": 0,
            "title": "Collection of client information",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Analyze client information",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Review of prior audit reports",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Engagement risk assessment",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "risk",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Fraud risk assessment",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Data analytics",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Identification of laws",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Benchmarking",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Engagement scope",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Audit engagement letters",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "letter",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Engagement work program",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "program",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Audit kick off meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        }
    ]
    query: str = """
                   INSERT INTO public.std_template (
                        engagement,
                        reference,
                        title,
                        tests,
                        results,
                        observation,
                        attachments,
                        conclusion,
                        type,
                        prepared_by,
                        reviewed_by
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            ref = 1
            for value in values:
                cursor.execute(query, (
                    engagement,
                    f"REF-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    value["type"],
                    json.dumps(value["prepared_by"]),
                    json.dumps(value["reviewed_by"]),
                ))
                ref = ref + 1

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding planning procedures {e}")

def reporting_procedures(connection: Connection, engagement: int):
    values = [
        {
            "title": "Summary of audit findings",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "finding",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Summary of audit process and rating",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "audit_process",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Finding sheet and management letter",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "sheet",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Exit meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Draft audit report",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Final audit report",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Updating audit findings",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Audit closure meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Circulation of final audit report",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
    ]
    query: str = """
                   INSERT INTO public.reporting_procedure (
                        engagement,
                        reference,
                        title,
                        tests,
                        results,
                        observation,
                        attachments,
                        conclusion,
                        type,
                        prepared_by,
                        reviewed_by
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            ref = 1
            for value in values:
                cursor.execute(query, (
                    engagement,
                    f"REF-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    value["type"],
                    json.dumps(value["prepared_by"]),
                    json.dumps(value["reviewed_by"]),
                ))
                ref = ref + 1

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding report procedures {e}")

def finalization_procedures(connection: Connection, engagement: int):
    values = [
        {
            "title": "Audit feedback process",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "survey",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Post audit meeting",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Closure of audit file",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "standard",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
        {
            "title": "Archive file",
            "tests": {
                "value": ""
            },
            "results": {
                "value": ""
            },
            "observation": {
                "value": ""
            },
            "attachments": [
                ""
            ],
            "conclusion": {
                "value": ""
            },
            "type": "archive",
            "prepared_by": {
                "id": 0,
                "name": ""
            },
            "reviewed_by": {
                "id": 0,
                "name": ""
            }
        },
    ]
    query: str = """
                   INSERT INTO public.finalization_procedure (
                        engagement,
                        reference,
                        title,
                        tests,
                        results,
                        observation,
                        attachments,
                        conclusion,
                        type,
                        prepared_by,
                        reviewed_by
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            ref = 1
            for value in values:
                cursor.execute(query, (
                    engagement,
                    f"REF-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    value["type"],
                    json.dumps(value["prepared_by"]),
                    json.dumps(value["reviewed_by"]),
                ))
                ref = ref + 1

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding finalization procedures {e}")

def add_engagement_profile(connection: Connection, engagement: int):
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
                   ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    try:
        values = (
            engagement,
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            json.dumps({
                "value": ""
            }),
            [""],
            json.dumps({
                "value": ""
            })
        )
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement profile {e}")