import time
import traceback
import uuid
from urllib.parse import urlencode

from fastapi import FastAPI, Depends, Form, Response, Request, Query
from starlette.responses import JSONResponse, RedirectResponse

from AuditNew.Internal.annual_plans.routes import router as annual_plans_router
from Management.entity.routes import router as entity
from AuditNew.Internal.engagements.routes import router as engagements_router
from Management.organization.databases import get_user_organizations
from Management.organization.schemas import Organization
from Management.roles.routes import router as roles_router
from Management.company_modules.routes import router as company_modules_router
from Management.entity.profile.risk_maturity_rating.routes import router as risk_maturity
from Management.entity.profile.control_weakness_rating.routes import router as control_weakness
from Management.entity.profile.issue_source.routes import router as issue_source
from Management.entity.profile.opinion_rating.routes import router as opinion_rating
from Management.entity.profile.control_effectiveness_rating.routes import router as control_effectiveness
from Management.entity.profile.control_type.routes import router as control_type_
from Management.entity.profile.risk_rating.routes import router as risk_rating_
from Management.entity.profile.business_process.routes import router as business_process_
from Management.entity.profile.impact_category.routes import router as impact_category_
from Management.entity.profile.engagement_type.routes import router as engagement_type
from AuditNew.Internal.engagements.administration.routes import router as administration_router
from AuditNew.Internal.engagements.work_program.routes import router as work_program_router
from AuditNew.Internal.engagements.finalizations.routes import router as finalization_router
from AuditNew.Internal.engagements.issue.routes import router as issue_
from AuditNew.Internal.engagements.task.routes import router as task_
from Management.entity.profile.root_cause_category.routes import router as root_cause
from Management.entity.profile.risk_category.routes import router as risk_category_
from AuditNew.Internal.engagements.review_comment.routes import router as review_comment_
from AuditNew.Internal.engagements.reporting.routes import router as reporting_router
from AuditNew.Internal.engagements.planning.routes import router as planning_router
from AuditNew.Internal.engagements.fieldwork.routes import router as fieldwork_router
from AuditNew.Internal.engagements.risk.routes import router as risk_
from AuditNew.Internal.dashboards.routes import router as dashboards
from AuditNew.Internal.engagements.control.routes import router as control_
from Management.users.routes import router as users_router
from Management.organization.routes import router as organization
from AuditNew.Internal.engagements.attachments.routes import router as attachments
from AuditNew.Internal.reports.routes import router as reports
from contextlib import asynccontextmanager
from redis_cache import init_redis_pool, close_redis_pool, get_redis_connection, redis_queue, return_redis_connection
from schema import CurrentUser, ResponseMessage, TokenResponse, LoginResponse, RedirectUrl
from utils import verify_password, create_jwt_token, get_async_db_connection, connection_pool_async, get_current_user, \
    update_user_password, generate_user_token, connection_pool_async_
from Management.users.databases import get_user_by_email
from fastapi.middleware.cors import CORSMiddleware
from Management.entity.databases import get_entities, get_entities_by_email
from Management.templates.databases import *
from dotenv import load_dotenv
import sys
import asyncio
from rate_limiter import RateLimiterMiddleware

load_dotenv()


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@asynccontextmanager
async def lifespan(api: FastAPI):
    try:
        #asyncio.create_task(smtp_worker())
        await init_redis_pool()
        await connection_pool_async.open()
        print("System booted successfully")
    except Exception as e:
        print(e)

    yield

    try:
        await close_redis_pool()
        await connection_pool_async.close()
        print("System shutdown successfully")
    except Exception as e:
        print(e)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"{e}"})

app.add_middleware(RateLimiterMiddleware, max_requests=500, window_seconds=60)

@app.get("/")
async def home(db=Depends(get_async_db_connection)):
    print(db)
    return ""

@app.post("/testing/{company_id}")
async def tester(
        company_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    start = time.perf_counter()
    data = await get_entities(connection=db, entity_id=company_id)
    end = time.perf_counter()
    return {
        "data": data,
        "time_taken": end - start
    }

@app.get("/session/{module_id}", tags=["Authentication"], response_model=RedirectUrl)
async def module_redirection(
        module_id: str,
        request: Request,
        sub_domain: str = Query(...),
        user: CurrentUser = Depends(get_current_user),
        db = Depends(get_async_db_connection)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    data: CurrentUser = await generate_user_token(connection=db, module_id=module_id, user_id=user.user_id)
    token: str = create_jwt_token(data.model_dump())
    session_code = str(uuid.uuid4())

    # Store in Redis with 5-minute expiry
    redis_conn = await get_redis_connection()
    try:
        await redis_conn.set(session_code, token, ex=300)  # ex = seconds
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while refresh token {e}")
    finally:
        await return_redis_connection(redis_conn) # Return to pool

    # Redirect with session_code
    redirect_url = f"https://{sub_domain}.{request.url.hostname}/auth?session_code={session_code}"
    return RedirectUrl(redirect_url=redirect_url)


@app.get("/api/session-code/{session_code}", tags=["Authentication"], response_model=TokenResponse)
async def refresh_token(
        session_code: str,
):
    redis_conn = await get_redis_connection()
    try:
        token = await redis_conn.get(session_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while refresh token {e}")
    finally:
        await return_redis_connection(redis_conn)  # Return to pool
    return TokenResponse(token=token)

@app.get("/token/{module_id}", tags=["Authentication"], response_model=TokenResponse)
async def get_token(
        module_id: str,
        response: Response,
        request: Request,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    data: CurrentUser = await generate_user_token(connection=db, module_id=module_id, user_id=user.user_id)
    token: str = create_jwt_token(data.model_dump())
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="lax",
        domain=request.url.hostname
    )
    return TokenResponse(token=token)

@app.post("/login", tags=["Authentication"], response_model=LoginResponse)
async def login(
          email: str = Form(...),
          password: str = Form(...),
          db=Depends(get_async_db_connection)):
    user_data  = await get_user_by_email(connection=db, email=email)
    if user_data.__len__() == 0:
        raise HTTPException(status_code=400, detail="User doesn't exists")
    password_hash: bytes = user_data[0].get("password_hash").encode()
    if verify_password(password_hash, password):
        user_ = CurrentUser(
            user_id = user_data[0].get("id"),
            user_name=user_data[0].get("name"),
            user_email=user_data[0].get("email"),
            entity_id=user_data[0].get("entity")
        )
        data = await get_user_organizations(connection=db, user_id=user_data[0].get("id"))
        organizations = [Organization(**p) for p in data]
        token = create_jwt_token(user_.model_dump())

        login_response = LoginResponse (
            user_id=user_data[0].get("id"),
            entity_id=user_data[0].get("entity"),
            name= user_data[0].get("name"),
            email= user_data[0].get("email"),
            telephone=user_data[0].get("telephone"),
            administrator=user_data[0].get("administrator"),
            owner=user_data[0].get("owner"),
            organizations= organizations,
            token=token
        )
        return login_response
    else:
        raise HTTPException(detail="Invalid password", status_code=400)

@app.put("/change_password", tags=["Authentication"])
async def change_password(
        old_password: str = Form(...),
        new_password: str = Form(...),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await update_user_password(
            connection=db,
            user_id=user.user_id,
            old_password=old_password,
            new_password=new_password)
        return ResponseMessage(detail="Password updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

app.include_router(entity, tags=["Entity"])
app.include_router(organization, tags=["Organization"])
app.include_router(company_modules_router, tags=["Modules"])
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
app.include_router(dashboards, tags=["System Dashboards"])
app.include_router(reports, tags=["System Reports"])
app.include_router(attachments, tags=["Attachments"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
