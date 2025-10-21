import json
from fastapi import HTTPException
from psycopg import AsyncConnection, sql
import logging
import uuid

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

def get_unique_key_():
    uuid_str = str(uuid.uuid4()).split("-")
    key = uuid_str[0] + uuid_str[1]
    return key

logging.basicConfig(
    filename="app.log",                   # Log file path
    filemode="a",                         # Append mode; use 'w' to overwrite each time
    level=logging.INFO,                   # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def engagement_types(company: str, connection: AsyncConnection):
    values = [
        "Internal Audit",
        "Compliance Audit",
        "Operational Audit",
        "IT Audit",
        "Forensic Audit",
        "Financial Audit",
        "Performance Audit",
        "Environmental Audit",
        "Tax Audit",
    ]
    query = sql.SQL(
        """
        INSERT INTO public.engagement_types (id, company, values)
        VALUES(%s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key_(),
                company,
                values
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def risk_rating(connection: AsyncConnection, company: str):
    values = [
        {"name": "Very High Risk", "magnitude": 4},
        {"name": "High Risk", "magnitude": 3},
        {"name":"Medium Risk", "magnitude": 2},
        {"name":"Low Risk", "magnitude": 1}
    ]
    query = sql.SQL(
        """
        INSERT INTO public.risk_rating (id, company, values)
        VALUES(%s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, json.dumps(values)))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def issue_finding_source(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.issue_source (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values = [
    "Internal Audit",
    "External Audit",
    "Self Disclosed",
    "Regulator Audit/Examination",
    "Other Assurance Reviews"]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def control_effectiveness_rating(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.control_effectiveness_rating (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values = [
    "Effective",
    "Partially Effective",
    "Ineffective"]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def control_weakness_rating(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.control_weakness_rating (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values = [
        "Acceptable",
        "Improvement Required",
        "Significant Improvement Required",
        "Unacceptable"
    ]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def audit_opinion_rating(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.opinion_rating (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values =  [
    "High Assurance",
    "Reasonable Assurance",
    "Limited Assurance",
    "No Assurance"]

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def risk_maturity_rating(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.risk_maturity_rating (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values =  [
    "Risk naive",
    "Risk aware",
    "Risk defined",
    "Risk managed"]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def control_type(connection: AsyncConnection, company: str):
    query = sql.SQL(
        """
        INSERT INTO public.control_type (id, company, values)
        VALUES (%s, %s, %s)
        """)
    values = [
    "Preventive control",
    "Detective control",
    "Corrective control",
    "Compensating control"]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (get_unique_key_(), company, values))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def roles(connection: AsyncConnection, company: str):
    value = [
        {
            "name": "Owner",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Admin",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Client",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Chief Executive Officer",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Chief Financial Officer",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Chief Information Officer",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Chief Operation Officer",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Chief Information Security Officer",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Head of Audit",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Senior Audit Manager",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        },
        {
            "name": "Risk Manager",
            "permissions": {
                "annual_audit_plan": ["create", "read", "update", "delete", "assign", "approve"],
                "engagements": ["create", "read", "update", "delete", "assign", "approve"],
                "administration": ["create", "read", "update", "delete", "assign", "approve"],
                "planning": ["create", "read", "update", "delete", "assign", "approve"],
                "fieldwork": ["create", "read", "update", "delete", "assign", "approve"],
                "finalization": ["create", "read", "update", "delete", "assign", "approve"],
                "reporting": ["create", "read", "update", "delete", "assign", "approve"],
                "work_program": ["create", "read", "update", "delete", "assign", "approve"]
            }

        }
    ]
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO public.roles (id, roles, company) VALUES (%s, %s, %s);",(
                    get_unique_key_(),
                    json.dumps(value),
                    company
                )
            )
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def business_process(connection: AsyncConnection, company: str):
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
    try:
        async with connection.cursor() as cursor:
            process_ids = {}
            query = sql.SQL(
                """
                INSERT INTO public.business_sub_process 
                (id, business_process, values) 
                VALUES (%s, %s, %s);
                """)

            for process in data:
                await cursor.execute(
                    "INSERT INTO public.business_process (id, name, code, company) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (get_unique_key_(), process["name"], process["code"], company)
                )
                process_id = await cursor.fetchone()
                process_ids[process["name"]] = process_id[0]  # Store process ID

            for process in data:
                process_id = process_ids[process["name"]]
                await cursor.execute(query, (get_unique_key_(), process_id, process["sub"]))

        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def root_cause_category(connection: AsyncConnection, company: str):
    data = [
    {
        "name": "People",
        "sub": [
            "Lack of Training & Knowledge gap",
            "Inadequate Supervision & Oversight by management/leaders",
            "Carelessness or Negligence",
            "Misinterpretation of Policies & Procedures"
        ]
    },
    {
        "name": "Governance",
        "sub": [
            "Unclear Roles & Responsibilities",
            "Inadequate organization structures",
            "Poor Communication & Coordination (Top-down)",
            "Weak Governance & Decision-Making",
            "Absence of identified policy/frameworks"
        ]
    },
    {
        "name": "Technology / Systems",
        "sub": [
            "Outdated or Inadequate Systems",
            "System Configuration & Integration Issues",
            "IT Security & Data Integrity Issues",
            "Insufficient Automation & Digitalization"
        ]
    },
    {
        "name": "Process",
        "sub": [
            "Incomplete or Undefined Processes",
            "Ineffective Controls & Monitoring",
            "Lack of Standard Operating Procedures (SOPs)",
            "Process Bottlenecks & Inefficiencies"
        ]
    },
    {
        "name": "Financial",
        "sub": [
            "Budgeting & Forecasting Errors",
            "Cash Flow Management Issues",
            "Cost Overruns & Uncontrolled Expenses",
            "Unclear applicable Financial Reporting Errors",
            "Resource Constraints & Capacity Issues"
        ]
    },
    {
        "name": "External factors",
        "sub": [
            "Lack of Awareness of Regulations & Policies",
            "Failure to Adapt to Regulatory Changes",
            "Natural calamities",
            "Pandemic outbreak",
            "Market changes"
        ]
    }
]
    try:
        async with connection.cursor() as cursor:
            process_ids = {}
            query = sql.SQL(
                """
                INSERT INTO public.root_cause_sub_category 
                (id, root_cause_category, values) 
                VALUES (%s, %s, %s);
                """)

            # 1️⃣ Insert Business Processes & Get Their IDs
            for process in data:
                await cursor.execute(
                    "INSERT INTO public.root_cause_category (id, name, company) VALUES (%s, %s, %s) RETURNING id;",
                    (get_unique_key_(), process["name"], company)
                )
                process_id = await cursor.fetchone()
                process_ids[process["name"]] = process_id[0]

            for process in data:
                process_id = process_ids[process["name"]]
                await cursor.execute(query, (get_unique_key_(), process_id, process["sub"]))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def risk_category(connection: AsyncConnection, company: str):
    data = [
    {
        "name": "Operational Risk",
        "sub": [
            "Process & Control Failures",
            "Human Resource Issues",
            "Technology & IT Risk",
            "Supply Chain & Vendor Risk"
        ]
    },
    {
        "name": "Compliance / Regulatory Risk",
        "sub": [
            "Legal & Regulatory Violations",
            "Tax Compliance Risk",
            "Data Privacy & Protection Risk",
            "Environmental, Social, and Governance (ESG) Risk",
            "Other industry specific regulation"
        ]
    },
    {
        "name": "Strategic Risk",
        "sub": [
            "Inappropriate Business Model",
            "Market Positioning Risk",
            "Mergers & Acquisitions Risk",
            "Competitive Risk",
            "Innovation & Technological Obsolescence Risk"
        ]
    },
    {
        "name": "Technology Risk",
        "sub": [
            "Data Breach & Cyber Threats",
            "System Downtime & Disruptions",
            "IT Governance & Security Compliance Risk",
            "Emerging Technology Risk",
            "Change management issues",
            "IT operations issues",
            "Access management",
            "IT security"
        ]
    },
    {
        "name": "Credit Risk",
        "sub": [
            "Default Risk",
            "Counterparty Risk",
            "Concentration Risk",
            "Country & Sovereign Risk"
        ]
    },
    {
        "name": "Liquidity Risk",
        "sub": [
            "Funding Liquidity Risk",
            "Market Liquidity Risk",
            "Asset Liquidity Risk",
            "Cash Flow Mismatch Risk"
        ]
    },
    {
        "name": "Market Risk",
        "sub": [
            "Interest Rate Risk",
            "Foreign Exchange Risk",
            "Commodity Price Risk",
            "Equity Price Risk"
        ]
    }
]

    try:
        async with connection.cursor() as cursor:
            process_ids = {}
            query = sql.SQL(
                """
                INSERT INTO public.sub_risk_category 
                (id, risk_category, values) 
                VALUES (%s, %s, %s);
                """)

            # 1️⃣ Insert Business Processes & Get Their IDs
            for process in data:
                await cursor.execute(
                    "INSERT INTO public.risk_category (id, name, company) VALUES (%s, %s, %s) RETURNING id;",
                    (get_unique_key_(), process["name"], company)
                )
                process_id = await cursor.fetchone()
                process_ids[process["name"]] = process_id[0]  # Store process ID

            for process in data:
                process_id = process_ids[process["name"]]
                await cursor.execute(query, (get_unique_key_(), process_id, process["sub"]))

            await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def impact_category(connection: AsyncConnection, company: str):
    data = [
    {
        "name": "Financial Impact",
        "sub": [
            "Monetary Loss (Direct financial loss due to fraud, errors, or mismanagement)",
            "Revenue Leakage (Loss of potential income due to process inefficiencies or compliance failures)",
            "Cost Overruns (Uncontrolled expenses beyond budget allocations)",
            "Financial Misstatement (Errors in financial reporting affecting decision-making)",
            "Liquidity Constraints (Cash flow issues impacting operations)"
        ]
    },
    {
        "name": "Compliance & Regulatory Impact",
        "sub": [
            "Legal Violations (Non-compliance with laws leading to penalties)",
            "Regulatory Fines & Sanctions (Government or industry-imposed fines)",
            "Tax Penalties (Failure to adhere to tax regulations)",
            "Licensing & Accreditation Issues (Loss of business licenses or certifications)",
            "ESG & Sustainability Issues"
        ]
    },
    {
        "name": "Operational Impact",
        "sub": [
            "Process Inefficiencies (Delays, redundancies, or workflow gaps)",
            "Disruptions in Business Continuity (Unplanned downtime or system failures)",
            "Resource Misallocation (Poor use of human or financial resources)",
            "Poor Service Delivery (Reduced productivity and performance)",
            "Supply Chain Interruptions (Delays due to vendor issues or logistical failures)"
        ]
    },
    {
        "name": "Reputational Impact",
        "sub": [
            "Public Trust & Brand Image Damage (Negative media coverage or public perception)",
            "Customer Dissatisfaction (Loss of clients due to service failures)",
            "Investor & Stakeholder Confidence (Reduced market value or shareholder trust)",
            "Ethical Violations & Social Responsibility Issues (Moral concerns affecting corporate standing)"
        ]
    },
    {
        "name": "Strategic & Governance Impact",
        "sub": [
            "Poor Decision-Making (Incorrect data leading to flawed strategies)",
            "Business Model Risks (Failure to adapt to market changes)",
            "Weak Corporate Governance (Lack of oversight and accountability)",
            "Loss of Competitive Advantage (Falling behind industry trends or innovations)"
        ]
    }
]

    try:
        async with connection.cursor() as cursor:
            process_ids = {}
            query = sql.SQL(
                """
                INSERT INTO public.impact_sub_category 
                (id, impact_category, values) 
                VALUES (%s, %s, %s);
                """)

            for process in data:
                await cursor.execute(
                    "INSERT INTO public.impact_category (id, name, company) VALUES (%s, %s, %s) RETURNING id;",
                    (get_unique_key_(), process["name"], company)
                )
                process_id = await cursor.fetchone()
                process_ids[process["name"]] = process_id[0]

            for process in data:
                process_id = process_ids[process["name"]]
                await cursor.execute(query, (get_unique_key_(), process_id, process["sub"]))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)

async def planning_procedures(connection: AsyncConnection, engagement_id: str):
    values =  [
    {
        "title": "Audit mobilization meeting",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Client notification",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Collection & Analyze of client information",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Review of prior audit reports",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Engagement risk assessment",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "risk",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Fraud risk assessment",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Data analytics",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Identification of laws",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Benchmarking",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Engagement scope",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Audit engagement letters",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "letter",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Engagement work program",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "program",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Audit kick off meeting",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    }
]

    query = sql.SQL(
        """
        INSERT INTO public.std_template (
            id,
            engagement,
            reference,
            title,
            tests,
            results,
            observation,
            attachments,
            conclusion,
            objectives,
            type,
            prepared_by,
            reviewed_by,
            status
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            ref = 1
            for value in values:
                await cursor.execute(query, (
                    get_unique_key_(),
                    engagement_id,
                    f"PLN-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    json.dumps(value["objectives"]),
                    value["type"],
                    None,
                    None,
                    "Pending"
                ))
                ref = ref + 1

        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)
        raise HTTPException(status_code=400, detail="Error creating planning procedure")

async def reporting_procedures(connection: AsyncConnection, engagement_id: str):
    values = [
    {
        "title": "Summary of audit findings",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "finding",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Summary of audit process and rating",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "audit_process",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Finding sheet and management letter",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "sheet",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Exit meeting",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Draft audit report",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Final  audit report & Circulation",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "circulate",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Updating audit findings",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    }
]

    query = sql.SQL(
        """
        INSERT INTO public.reporting_procedure (
            id,
            engagement,
            reference,
            title,
            tests,
            results,
            observation,
            attachments,
            conclusion,
            objectives,
            type,
            prepared_by,
            reviewed_by,
            status
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            ref = 1
            for value in values:
                await cursor.execute(query, (
                    get_unique_key_(),
                    engagement_id,
                    f"RPT-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    json.dumps(value["objectives"]),
                    value["type"],
                    None,
                    None,
                    "Pending"
                ))
                ref = ref + 1

        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)
        raise HTTPException(status_code=400, detail=f"Error adding report procedures {e}")

async def finalization_procedures(connection: AsyncConnection, engagement_id: str):
    values = [
    {
        "title": "Timesheet & audit resource utilization",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "timesheet",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Audit feedback process",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "survey",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Audit closure meeting",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "standard",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Closure of audit file",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "closure",
        "prepared_by": None,
        "reviewed_by": None
    },
    {
        "title": "Archive file",
        "tests": {"value": ""},
        "results": {"value": ""},
        "observation": {"value": ""},
        "attachments": [""],
        "conclusion": {"value": ""},
        "objectives": {"value": ""},
        "type": "archive",
        "prepared_by": None,
        "reviewed_by": None
    }
]
    query = sql.SQL(
        """
        INSERT INTO public.finalization_procedure (
            id,
            engagement,
            reference,
            title,
            tests,
            results,
            observation,
            attachments,
            conclusion,
            objectives,
            type,
            prepared_by,
            reviewed_by,
            status
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            ref = 1
            for value in values:
                await cursor.execute(query, (
                    get_unique_key_(),
                    engagement_id,
                    f"FNL-{ref:04d}",
                    value["title"],
                    json.dumps(value["tests"]),
                    json.dumps(value["results"]),
                    json.dumps(value["observation"]),
                    value["attachments"],
                    json.dumps(value["conclusion"]),
                    json.dumps(value["objectives"]),
                    value["type"],
                    None,
                    None,
                    "Pending"
                ))
                ref = ref + 1

        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)
        raise HTTPException(status_code=400, detail=f"Error adding finalization procedures {e}")

async def add_engagement_profile(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.profile (
            id,
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
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        values = (
            get_unique_key_(),
            engagement_id,
            json.dumps({}),  # audit_background
            json.dumps({}),  # audit_objectives
            json.dumps({}),  # key_legislations
            json.dumps({}),  # relevant_systems
            json.dumps({}),  # key_changes
            json.dumps({}),  # reliance
            json.dumps({}),  # scope_exclusion
            [],              # core risks
            json.dumps({})   # estimated_dates
        )
        async with connection.cursor() as cursor:
            await cursor.execute(query, values)
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        logger.error(e)
        raise HTTPException(status_code=400, detail=f"Error adding engagement profile {e}")

async def engagement_letter(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.engagement_letter (id, engagement, name, value, size, type, extension) VALUES(%s, %s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key_(),
                engagement_id,
                "",
                "",
                0,
                "final",
                ""
            ))
            await cursor.execute(query, (
                get_unique_key_(),
                engagement_id,
                "",
                "",
                0,
                "scoped",
                ""
            ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement letter {e}")