import tempfile

from fastapi import FastAPI, Depends, Form, BackgroundTasks
from AuditNew.Internal.annual_plans.routes import router as annual_plans_router
from Management.companies.routes import router as companies_router
from AuditNew.Internal.engagements.routes import router as engagements_router
from Management.roles.routes import router as roles_router
from Management.company_modules.routes import router as company_modules_router
from Management.companies.profile.risk_maturity_rating.routes import router as risk_maturity
from Management.companies.profile.control_weakness_rating.routes import router as control_weakness
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
from Management.companies.profile.root_cause_category.routes import router as root_cause
from Management.companies.profile.risk_category.routes import router as risk_category_
from AuditNew.Internal.engagements.review_comment.routes import router as review_comment_
from AuditNew.Internal.engagements.reporting.routes import router as reporting_router
from AuditNew.Internal.engagements.planning.routes import router as planning_router
from AuditNew.Internal.engagements.fieldwork.routes import router as fieldwork_router
from AuditNew.Internal.engagements.risk.routes import router as risk_
from AuditNew.Internal.engagements.control.routes import router as control_
from Management.users.routes import router as users_router
from contextlib import asynccontextmanager
from utils import verify_password, get_db_connection, create_jwt_token, get_async_db_connection, connection_pool_async, \
    check_permission,  query_any_data
from Management.users.databases import get_user_by_email
from fastapi.middleware.cors import CORSMiddleware
from Management.companies.databases import  get_companies
from rabbitmq import rabbitmq
from Management.templates.databases import *
from dotenv import load_dotenv
import sys
import asyncio
from rate_limiter import RateLimiterMiddleware

load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    from utils import connection_pool
    if connection_pool:
        #rabbitmq.connect(queue_name="task")
        #consumer_thread = threading.Thread(target=rabbitmq.consume_messages, args=("task",), daemon=True)
        #consumer_thread.start()
        print("Database connection sync pool initialized.")

    await connection_pool_async.open()
    if connection_pool_async:
        print("Database connection async pool initialized.")
    yield
    from utils import connection_pool
    connection_pool.closeall()
    await connection_pool_async.close()
    rabbitmq.close()
    print("Database connection sync pool closed")
    print("Database connection async pool closed")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(RateLimiterMiddleware, max_requests=10, window_seconds=60)

from fastapi import UploadFile, File
import os
from psycopg.errors import UniqueViolation
from s3 import upload_file
import shutil
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/test")
async def tester(
        file: UploadFile = File(...),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        db_async= Depends(get_async_db_connection),
        #per = Depends(check_permission(module="planning", action= "c"))
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name

        key: str = f"annual_plans/{file.filename}"
        public_url: str = f"https://egarc.s3.us-east-1.amazonaws.com/{key}"
        background_tasks.add_task(upload_file, temp_path, key)
        print(public_url)
    except HTTPException as h:
        raise HTTPException(status_code=h.status_code, detail=h.detail)
    # print(file.filename)
    # file_location = os.path.join(UPLOAD_DIR, file.filename)
    #
    # with open(file_location, "wb") as f:
    #     shutil.copyfileobj(file.file, f)

@app.post("/login", tags=["Authentication"])
async def login(
          email: str = Form(...),
          password: str = Form(...),
          db=Depends(get_async_db_connection)):
    user_data  = await get_user_by_email(connection=db, email=email)
    if len(user_data) == 0:
        raise HTTPException(status_code=400, detail="User doesn't exists")
    password_hash: bytes = user_data[0]["password_hash"].encode()
    company = await get_companies(db, company_id=user_data[0].get("company"))
    if verify_password(password_hash, password):
        user: dict = {
            "user_id": user_data[0].get("id"),
            "user_email": user_data[0].get("email"),
            "user_name": user_data[0].get("name"),
            "company_id": user_data[0].get("company"),
            "company_name": company[0].get("name"),
            "type": user_data[0].get("type"),
            "status": user_data[0].get("status")
        }

        token: str = create_jwt_token(user)
        user: dict = {
            "id": user_data[0].get("id"),
            "name": user_data[0].get("name"),
            "email": user_data[0].get("email"),
            "company_name": company[0].get("name"),
            "account_status": company[0].get("status"),
            "role": user_data[0].get("role"),
            "module": user_data[0].get("module")
        }
        return {"token": token, "token_type": "Bearer", "status_code": 203, "detail": "login success", "content": user}
    else:
        raise HTTPException(detail="Invalid password", status_code=400)

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
app.include_router(issue_source, tags=["Issue Source"])
app.include_router(opinion_rating, tags=["Opinion Rating"])
app.include_router(engagement_type, tags=["Engagement Types"])
app.include_router(control_effectiveness, tags=["Control Effectiveness Rating"])
app.include_router(control_type_, tags=["Control Type"])
app.include_router(risk_rating_, tags=["Risk rating"])
app.include_router(business_process_, tags=["Engagement Business Processes"])
app.include_router(impact_category_, tags=["Impact Category Rating"])
app.include_router(root_cause, tags=["Root Cause Category"])
app.include_router(risk_category_, tags=["Risk Category Rating"])
app.include_router(issue_, tags=["Issue"])
app.include_router(task_, tags=["Task"])
app.include_router(review_comment_, tags=["Review Comment"])
app.include_router(risk_, tags=["Engagement Risk"])
app.include_router(control_, tags=["Engagement Control"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

