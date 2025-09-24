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
    ISSUES = "issues"
    RISK_CONTROL = "risk_control"
