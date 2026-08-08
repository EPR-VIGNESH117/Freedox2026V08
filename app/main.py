from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
# Import models to ensure they are registered with Base metadata
from app.models import FacultyMember, FacultyQualification  # noqa: F401
from app.api.v1.router import api_router

# Ensure tables exist on startup if running without migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## Faculty Qualification Review Platform API

    A RESTful backend service designed to store, manage, filter, and analyze faculty credentials and qualifications across academic departments.

    ### Features:
    * **Faculty Management**: Complete CRUD operations for faculty members.
    * **Multi-Qualification Support**: Assign multiple qualifications (B.Tech, M.Tech, PhD, M.Sc, MBA) to individual faculty members via normalized relational entities.
    * **Advanced Filtering**: Search and filter by department, designation, degree qualification, and years of experience.
    * **Analytical Reports**: Real-time analytical reports grouped by **Department**, **Qualification**, **Designation**, and **Experience Brackets**.
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_v1_url": f"{settings.API_V1_STR}"
    }
