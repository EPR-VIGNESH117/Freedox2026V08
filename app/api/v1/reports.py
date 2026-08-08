from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.report import (
    DepartmentReportResponse,
    QualificationReportResponse,
    DesignationReportResponse,
    ExperienceReportResponse,
)
from app.crud import report as crud_report

router = APIRouter()

@router.get("/department", response_model=DepartmentReportResponse, summary="Get department analytical report")
def get_department_analytics(db: Session = Depends(get_db)):
    return crud_report.get_department_report(db)

@router.get("/qualification", response_model=QualificationReportResponse, summary="Get qualification analytical report")
def get_qualification_analytics(db: Session = Depends(get_db)):
    return crud_report.get_qualification_report(db)

@router.get("/designation", response_model=DesignationReportResponse, summary="Get designation analytical report")
def get_designation_analytics(db: Session = Depends(get_db)):
    return crud_report.get_designation_report(db)

@router.get("/experience", response_model=ExperienceReportResponse, summary="Get experience brackets report")
def get_experience_analytics(db: Session = Depends(get_db)):
    return crud_report.get_experience_report(db)
