from enum import Enum


class Tables(str, Enum):
    ENTITIES = "entities"
    ORGANIZATIONS  = "organizations"
    MODULES = "modules"
    ENGAGEMENTS = "engagements"
    ANNUAL_PLANS = "annual_plans"
    USERS  = "users"
    ORGANIZATIONS_USERS = "organizations_users"
    MODULES_USERS = "modules_users"
    ACTIVATIONS = "activations"
    AUDIT_LICENCES = "audit_licences"
    MAIN_PROGRAM = "main_program"
    SUB_PROGRAM = "sub_program"
    ISSUES = "issues"
    RISK_CONTROL = "risk_control"
    FOLLOW_UP = "follow_up"
