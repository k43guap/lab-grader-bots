from fastapi import FastAPI

from api_clients.course_sheet_manager import CourseSheetManager
from api_clients.github_manager import GithubManager
from api_clients.google.google_sheets_client import GoogleSheetClient, GoogleSheetSession
from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.routers import router as auth_router
from apps.grader.routers import router as grader_router
from config import get_settings, Settings

app = FastAPI(
    title="Lab Grader",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup() -> None:
    settings = Settings()

    google_sheet_session = GoogleSheetSession(settings)
    await google_sheet_session.init_session()
    course_sheet_manager = CourseSheetManager(google_sheets_client=GoogleSheetClient(google_sheet_session))

    github_manager = GithubManager(settings)

    app.dependency_overrides = {
        get_settings: lambda: settings,
        CourseSheetManagerProtocol: lambda: course_sheet_manager,
        GithubManagerProtocol: lambda: github_manager,
    }

app.include_router(auth_router, tags=["Authorization"], prefix="/api/authorization")
app.include_router(grader_router, tags=["Grader"], prefix="/api/grader")
