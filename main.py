from pathlib import Path

from fastapi import FastAPI, Depends, Form, File, UploadFile
from AuditNew.Internal.annual_plans.routes import router as annual_plans_router
from Management.companies.routes import router as companies_router
from AuditNew.Internal.engagements.routes import router as engagements_router
from Management.roles.routes import router as roles_router
from Management.company_modules.routes import router as company_modules_router
from Management.settings.engagement_types.routes import router as engagement_types_router
from Management.companies.profile.risk_maturity_rating.routes import router as risk_maturity
from Management.companies.profile.control_weakness_rating.routes import router as control_weakness
from Management.companies.profile.issue_implementation.routes import router as issue_implementation
from Management.companies.profile.issue_source.routes import router as issue_source
from Management.companies.profile.opinion_rating.routes import router as opinion_rating
from Management.companies.profile.control_effectiveness_rating.routes import router as control_effectiveness
from Management.companies.profile.control_type.routes import router as control_type_
from Management.companies.profile.risk_rating.routes import router as risk_rating_
from Management.companies.profile.business_process.routes import router as business_process_
from Management.companies.profile.impact_category.routes import router as impact_category_
from Management.companies.profile.engagement_type.routes import router as engagement_type
from AuditNew.Internal.engagements.administration.routes import router as administration_router
from AuditNew.Internal.engagements.work_program.routes import router as work_program_router
from AuditNew.Internal.engagements.finalizations.routes import router as finalization_router
from AuditNew.Internal.engagements.issue.routes import router as issue_
from AuditNew.Internal.engagements.task.routes import router as task_
from AuditNew.Internal.engagements.review_comment.routes import router as review_comment_
from AuditNew.Internal.engagements.reporting.routes import router as reporting_router
from AuditNew.Internal.engagements.planning.routes import router as planning_router
from AuditNew.Internal.engagements.fieldwork.routes import router as fieldwork_router
from Management.users.routes import router as users_router
from contextlib import asynccontextmanager
from utils import verify_password, get_db_connection, create_jwt_token
from Management.users.databases import get_user
from fastapi.middleware.cors import CORSMiddleware
from Management.companies.databases import  get_companies

from Management.templates.databases import *


from seedings import impact_category,risk_category,root_cause_category

@asynccontextmanager
async def lifespan(app: FastAPI):
    from utils import connection_pool
    if connection_pool:
        print("Database connection pool initialized.")
    yield
    from utils import connection_pool
    connection_pool.closeall()
    print("Database connection pool closed")

app = FastAPI(lifespan=lifespan)
from seedings import *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where files will be stored
UPLOAD_DIR = Path("/var/www/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/")
async def test(

        file: UploadFile = File(...),
        db=Depends(get_db_connection),
):
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file
    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    public_url = f"http://capstone.co.tz/files/{file.filename}"
    return {"filename": file.filename, "url": public_url}


@app.post("/login", tags=["Authentication"])
def users(
          email: str = Form(...),
          password: str = Form(...),
          db: Connection = Depends(get_db_connection)):
    user_data: List[Dict] = get_user(db, column="email", value=email)
    if len(user_data) == 0:
        return HTTPException(status_code=405, detail="User doesn't exists")
    password_hash: bytes = user_data[0]["password_hash"].encode()
    if verify_password(password_hash, password):
        user: dict = {
            "user_id": user_data[0].get("id"),
            "company_id": user_data[0].get("company"),
            "type": user_data[0].get("type"),
            "status": user_data[0].get("status")
        }
        company = get_companies(db, column="id", value=user_data[0].get("company_id"))[0]
        token: str = create_jwt_token(user)
        user: dict = {
            "id": user_data[0].get("id"),
            "name": user_data[0].get("name"),
            "email": user_data[0].get("email"),
            "company_name": company.get("name"),
            "account_status": company.get("status"),
            "role": user_data[0].get("role")
        }
        return {"token": token, "token_type": "bearer", "status_code": 203, "detail": "login success", "content": user}
    else:
        return {"detail":"Invalid password", "status_code": 204}

app.include_router(companies_router, tags=["Company"])
app.include_router(company_modules_router, tags=["Company Modules"])
app.include_router(users_router,tags=["User"])
app.include_router(annual_plans_router, tags=["Annual Audit Plans"])
app.include_router(engagements_router, tags=["Engagements"])
app.include_router(administration_router, tags=["Engagement Administration"])
app.include_router(planning_router, tags=["Engagement Planning"])
app.include_router(fieldwork_router, tags=["Engagement Fieldwork"])
app.include_router(finalization_router, tags=["Engagement Finalization"])
app.include_router(reporting_router, tags=["Engagement Reporting"])
app.include_router(work_program_router, tags=["Engagement Work Program"])
app.include_router(roles_router, tags=["Roles"])
app.include_router(risk_maturity, tags=["Risk Maturity Rating"])
app.include_router(control_weakness, tags=["Control Weakness Rating"])
app.include_router(issue_implementation, tags=["Issue Implementation"])
app.include_router(issue_source, tags=["Issue Source"])
app.include_router(opinion_rating, tags=["Opinion Rating"])
app.include_router(engagement_type, tags=["Engagement Types"])
app.include_router(control_effectiveness, tags=["Control Effectiveness Rating"])
app.include_router(control_type_, tags=["Control Type"])
app.include_router(risk_rating_, tags=["Risk rating"])
app.include_router(business_process_, tags=["Engagement Business Processes"])
app.include_router(impact_category_, tags=["Impact Category Rating"])
app.include_router(issue_, tags=["Issue"])
app.include_router(task_, tags=["Task"])
app.include_router(review_comment_, tags=["Review Comment"])


# app.include_router(modules_router, tags=["Modules"])
# app.include_router(templates_router, tags=["Templates"])
# app.include_router(audit_logs_router)
# app.include_router(engagement_profile_router)
# app.include_router(permission_router)
# app.include_router(features_router)
# app.include_router(feature_record_router)
# app.include_router(staff_assignment_router)
# app.include_router(planning_details_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
