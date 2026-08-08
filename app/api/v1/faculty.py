from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.faculty import (
    FacultyCreate,
    FacultyUpdate,
    FacultyResponse,
)
from app.schemas.qualification import (
    QualificationCreate,
    QualificationResponse,
)
from app.crud import faculty as crud_faculty
from app.crud import qualification as crud_qual

router = APIRouter()

@router.post("/faculty", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED, summary="Create a new faculty member")
def create_faculty_member(
    faculty_in: FacultyCreate,
    db: Session = Depends(get_db)
):
    existing = crud_faculty.get_faculty_by_email(db, email=faculty_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Faculty member with email '{faculty_in.email}' already exists."
        )
    return crud_faculty.create_faculty(db=db, faculty_in=faculty_in)

@router.get("/faculty", response_model=List[FacultyResponse], summary="Retrieve and filter faculty members")
def read_faculty_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    department: Optional[str] = Query(None, description="Filter by department name"),
    designation: Optional[str] = Query(None, description="Filter by designation name"),
    qualification: Optional[str] = Query(None, description="Filter by qualification degree e.g. PhD, M.Tech"),
    min_experience: Optional[int] = Query(None, ge=0, description="Minimum years of experience"),
    max_experience: Optional[int] = Query(None, ge=0, description="Maximum years of experience"),
    search: Optional[str] = Query(None, description="Search keyword in name or email"),
    db: Session = Depends(get_db)
):
    return crud_faculty.get_faculty_list(
        db=db,
        skip=skip,
        limit=limit,
        department=department,
        designation=designation,
        qualification=qualification,
        min_experience=min_experience,
        max_experience=max_experience,
        search=search
    )

@router.get("/faculty/{faculty_id}", response_model=FacultyResponse, summary="Get details of a specific faculty member")
def read_faculty_member(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    db_faculty = crud_faculty.get_faculty_by_id(db, faculty_id=faculty_id)
    if not db_faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found."
        )
    return db_faculty

@router.put("/faculty/{faculty_id}", response_model=FacultyResponse, summary="Update faculty member details")
def update_faculty_member(
    faculty_id: int,
    faculty_in: FacultyUpdate,
    db: Session = Depends(get_db)
):
    db_faculty = crud_faculty.get_faculty_by_id(db, faculty_id=faculty_id)
    if not db_faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found."
        )

    if faculty_in.email and faculty_in.email.strip().lower() != db_faculty.email.lower():
        existing_email = crud_faculty.get_faculty_by_email(db, email=faculty_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Faculty member with email '{faculty_in.email}' already exists."
            )

    updated = crud_faculty.update_faculty(db=db, faculty_id=faculty_id, faculty_in=faculty_in)
    return updated

@router.delete("/faculty/{faculty_id}", status_code=status.HTTP_200_OK, summary="Delete a faculty member")
def delete_faculty_member(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    success = crud_faculty.delete_faculty(db, faculty_id=faculty_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found."
        )
    return {"message": f"Faculty member with ID {faculty_id} successfully deleted."}

@router.post("/faculty/{faculty_id}/qualifications", response_model=QualificationResponse, status_code=status.HTTP_201_CREATED, summary="Add a qualification to a faculty member")
def add_faculty_qualification(
    faculty_id: int,
    qual_in: QualificationCreate,
    db: Session = Depends(get_db)
):
    db_faculty = crud_faculty.get_faculty_by_id(db, faculty_id=faculty_id)
    if not db_faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found."
        )
    return crud_qual.add_qualification(db=db, faculty_id=faculty_id, qual_in=qual_in)

@router.get("/faculty/{faculty_id}/qualifications", response_model=List[QualificationResponse], summary="Retrieve all qualifications for a specific faculty member")
def get_faculty_qualifications(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    db_faculty = crud_faculty.get_faculty_by_id(db, faculty_id=faculty_id)
    if not db_faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found."
        )
    return crud_qual.get_qualifications_by_faculty_id(db=db, faculty_id=faculty_id)

@router.get("/qualifications", response_model=List[QualificationResponse], summary="Retrieve all qualifications across all faculty members")
def read_all_qualifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_qual.get_all_qualifications(db=db, skip=skip, limit=limit)

@router.delete("/qualifications/{qualification_id}", status_code=status.HTTP_200_OK, summary="Delete a qualification entry")
def delete_qualification_entry(
    qualification_id: int,
    db: Session = Depends(get_db)
):
    success = crud_qual.delete_qualification(db, qualification_id=qualification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Qualification with ID {qualification_id} not found."
        )
    return {"message": f"Qualification with ID {qualification_id} successfully deleted."}
