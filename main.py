import uuid
from typing import Optional
from fastapi import FastAPI, Depends, Form, Request, Query, HTTPException
from starlette.responses import JSONResponse
from Management.roles.routes import router as roles_router
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
from AuditNew.Internal.engagements.task.routes import router as task_
from Management.entity.profile.root_cause_category.routes import router as root_cause
from Management.entity.profile.risk_category.routes import router as risk_category_
from AuditNew.Internal.engagements.review_comment.routes import router as review_comment_
from AuditNew.Internal.engagements.reporting.routes import router as reporting_router
from AuditNew.Internal.engagements.fieldwork.routes import router as fieldwork_router
from AuditNew.Internal.dashboards.routes import router as dashboards
from Management.subscriptions.routes import router as subscriptions
from routes.attachment_routes import router as attachment_routes
from AuditNew.Internal.reports.routes import router as reports
from contextlib import asynccontextmanager
from models.organization_models import get_user_organizations
from models.user_models import get_entity_user_details_by_mail
from schema import CurrentUser, ResponseMessage, TokenResponse, LoginResponse, RedirectUrl
from schemas.organization_schemas import ReadOrganization
from services.connections.rabitmq.connection import AsyncRabbitMQSingleton
from services.connections.rabitmq.consumer_thread import consumer
from services.logging.logger import global_logger
from services.security.security import verify_password
from utils import create_jwt_token, get_async_db_connection, get_current_user, \
    update_user_password, generate_user_token, generate_risk_user_token, exception_response
from dotenv import load_dotenv
import sys
import asyncio
from rate_limiter import RateLimiterMiddleware
from starlette.middleware.cors import CORSMiddleware
from core.datastructures.pop_dict import PopDict
from routes.issue_routes import router as issue_routes
from routes.library_routes import router as library_routes
from routes.notification_routes import router as notification_routes
from routes.entity_routes import router as entity_routes
from routes.organization_routes import router as organization_routes
from routes.module_routes import router as module_routes
from routes.user_routes import router as user_routes
from routes.annual_plan_routes import router as annual_plan_routes
from routes.engagement_routes import router as engagement_routes
from routes.follow_up_routes import router as follow_up_routes
from routes.main_program_routes import router as main_program_routes
from routes.sub_program_routes import router as sub_program_routes
from routes.engagement_staff_routes import router as engagement_staff_routes
from routes.issue_actor_routes import router as issue_actor_routes
from routes.PRCM_routes import router as PRCM_routes
from routes.engegement_administration_profile_routes import router as engagement_administration_profile_routes
from routes.risk_control_routes import router as risk_control_routes
from routes.management_routes import router as management_routes
from routes.policy_routes import router as policy_routes
from routes.regulation_routes import router as regulation_routes
from routes.engagement_process_routes import router as engagement_process_routes
from routes.standard_template_routes import router as standard_template_routes
from routes.planning_routes import router as planning_routes
from services.ai.base_ai import router as ai



load_dotenv()


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


session_storage = PopDict()

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        consumer.start()
    except Exception as e:
        print(e)
    yield

    try:
        await AsyncRabbitMQSingleton.get_instance().close_connection()
        consumer.stop()
    except Exception as e:
        print(e)





app = FastAPI(lifespan=lifespan)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as h:
        global_logger.error(h)
    except Exception as e:
        global_logger.error(e)
        return JSONResponse(status_code=500, content={"detail": str(e)})



# noinspection PyTypeChecker
app.add_middleware(RateLimiterMiddleware, max_requests=500, window_seconds=60)

@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    global_logger.error(f"HTTPException: {exc.detail} | Status Code: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/{engagement_id}")
async def home():
    with exception_response():
        pass




@app.get("/session/{module_id}", tags=["Authentication"], response_model=RedirectUrl)
async def module_redirection(
        module_id: str,
        request: Request,
        sub_domain: str = Query(...),
        user: CurrentUser = Depends(get_current_user),
        db = Depends(get_async_db_connection),
):

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)

    data: Optional[CurrentUser] = None
    if sub_domain == "eaudit":
        data: CurrentUser = await generate_user_token(connection=db, module_id=module_id, user_id=user.user_id)
    if sub_domain == "eRisk":
        data: CurrentUser = await generate_risk_user_token(connection=db, module_id=module_id, user_id=user.user_id)

    if data is None:
        raise HTTPException(status_code=400, detail="Unknown sub-domain")

    token: str = create_jwt_token(data.model_dump())
    session_code = str(uuid.uuid4())

    try:
        session_storage.put(session_code, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while refresh token {e}")

    if sub_domain == "eRisk":
        redirect_url = f"http://{request.headers.get('origin').split('//')[1]}/auth?session_code={session_code}"
        return RedirectUrl(redirect_url=redirect_url)
    else:
        redirect_url = f"http://{sub_domain}.{request.headers.get('origin').split('//')[1]}/auth?session_code={session_code}"
        return RedirectUrl(redirect_url=redirect_url)



@app.get("/api/session-code/{session_code}", tags=["Authentication"], response_model=TokenResponse)
async def refresh_token(
        session_code: str,
):
    try:
        token = session_storage.get(session_code)
        if token is None:
            raise HTTPException(status_code=400, detail=f"Unknown Session Code")

        return TokenResponse(token=token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while retrieving session code {e}")



@app.post("/login", tags=["Authentication"], response_model=LoginResponse)
async def login(
          email: str = Form(...),
          password: str = Form(...),
          connection=Depends(get_async_db_connection)
):
    with exception_response():

        user_data  = await get_entity_user_details_by_mail(
            connection=connection,
            email=email
        )

        if user_data is None:
            raise HTTPException(status_code=404, detail="User doesn't exists")

        password_hash = user_data.get("password_hash")
        if verify_password(password_hash, password):
            user_ = CurrentUser(
                user_id = user_data.get("id"),
                user_name=user_data.get("name"),
                user_email=user_data.get("email"),
                entity_id=user_data.get("entity")
            )

            data = await get_user_organizations(
                connection=connection,
                user_id=user_data.get("id")
            )

            organizations = [ReadOrganization(**p) for p in data]

            token = create_jwt_token(user_.model_dump())

            login_response = LoginResponse (
                user_id=user_data.get("id"),
                entity_id=user_data.get("entity"),
                name= user_data.get("name"),
                email= user_data.get("email"),
                telephone=user_data.get("telephone"),
                administrator=user_data.get("administrator"),
                owner=user_data.get("owner"),
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
            new_password=new_password
        )

        return ResponseMessage(detail="Password updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


app.include_router(administration_router, tags=["Engagement Administration"])
app.include_router(fieldwork_router, tags=["Engagement Fieldwork"])
app.include_router(reporting_router, tags=["Engagement Reporting"])
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
app.include_router(task_, tags=["Task"])
app.include_router(review_comment_, tags=["Review Comment"])
app.include_router(dashboards, tags=["System Dashboards"])
app.include_router(reports, tags=["System Reports"])


app.include_router(ai, tags=["AI Generation Routes"])
app.include_router(attachment_routes, tags=["Attachments Routes"])
app.include_router(subscriptions, tags=["Subscriptions"])
app.include_router(entity_routes, tags=["Entity Routes"])
app.include_router(organization_routes, tags=["Organization Routes"])
app.include_router(module_routes, tags=["Module Routes"])
app.include_router(user_routes, tags=["User Routes"])
app.include_router(annual_plan_routes, tags=["Annual Plans Routes"])
app.include_router(engagement_routes, tags=["Engagements Routes"])
app.include_router(engagement_administration_profile_routes, tags=["Engagement Administration Profile  Routes"])
app.include_router(policy_routes, tags=["Engagement Policies  Routes"])
app.include_router(regulation_routes, tags=["Engagement Regulations  Routes"])
app.include_router(engagement_process_routes, tags=["Engagement Process  Routes"])
app.include_router(engagement_staff_routes, tags=["Engagements Staff Routes"])
app.include_router(standard_template_routes, tags=["Standard Templates Procedure Routes"])
app.include_router(planning_routes, tags=["Planning  Routes"])


app.include_router(PRCM_routes, tags=["PRCM  Routes"])
app.include_router(issue_routes, tags=["Issue Routes"])
app.include_router(issue_actor_routes, tags=["Issue Actors Routes"])
app.include_router(risk_control_routes, tags=["Risk Control Routes"])
app.include_router(notification_routes, tags=["Notification Routes"])
app.include_router(library_routes, tags=["Library Routes"])
app.include_router(main_program_routes, tags=["Main Program Routes"])
app.include_router(sub_program_routes, tags=["Sub Program Routes"])
app.include_router(follow_up_routes, tags=["Follow Routes"])
app.include_router(management_routes, tags=["Management Routes"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
