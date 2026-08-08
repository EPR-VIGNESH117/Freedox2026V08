from fastapi import APIRouter
from app.api.v1.faculty import router as faculty_router
from app.api.v1.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(faculty_router, tags=["Faculty & Qualifications"])
api_router.include_router(reports_router, prefix="/reports", tags=["Analytical Reports"])
