from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.faculty import FacultyMember
from app.models.qualification import FacultyQualification
from app.schemas.faculty import FacultyCreate, FacultyUpdate

def create_faculty(db: Session, faculty_in: FacultyCreate) -> FacultyMember:
    db_faculty = FacultyMember(
        first_name=faculty_in.first_name.strip(),
        last_name=faculty_in.last_name.strip(),
        email=faculty_in.email.strip().lower(),
        department=faculty_in.department.strip(),
        designation=faculty_in.designation.strip(),
        years_of_experience=faculty_in.years_of_experience,
        joining_date=faculty_in.joining_date
    )
    db.add(db_faculty)
    db.flush()  # to populate db_faculty.id before creating qualifications

    if faculty_in.qualifications:
        for q in faculty_in.qualifications:
            db_qual = FacultyQualification(
                faculty_id=db_faculty.id,
                degree=q.degree.strip(),
                field_of_study=q.field_of_study.strip() if q.field_of_study else None,
                institution=q.institution.strip() if q.institution else None,
                passing_year=q.passing_year
            )
            db.add(db_qual)

    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def get_faculty_by_id(db: Session, faculty_id: int) -> Optional[FacultyMember]:
    return db.query(FacultyMember).filter(FacultyMember.id == faculty_id).first()

def get_faculty_by_email(db: Session, email: str) -> Optional[FacultyMember]:
    return db.query(FacultyMember).filter(func.lower(FacultyMember.email) == email.strip().lower()).first()

def get_faculty_list(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    department: Optional[str] = None,
    designation: Optional[str] = None,
    qualification: Optional[str] = None,
    min_experience: Optional[int] = None,
    max_experience: Optional[int] = None,
    search: Optional[str] = None
) -> List[FacultyMember]:
    query = db.query(FacultyMember).distinct()

    if qualification:
        query = query.join(FacultyMember.qualifications).filter(
            func.lower(FacultyQualification.degree) == qualification.strip().lower()
        )

    if department:
        query = query.filter(func.lower(FacultyMember.department) == department.strip().lower())

    if designation:
        query = query.filter(func.lower(FacultyMember.designation) == designation.strip().lower())

    if min_experience is not None:
        query = query.filter(FacultyMember.years_of_experience >= min_experience)

    if max_experience is not None:
        query = query.filter(FacultyMember.years_of_experience <= max_experience)

    if search:
        search_term = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(FacultyMember.first_name).like(search_term),
                func.lower(FacultyMember.last_name).like(search_term),
                func.lower(FacultyMember.email).like(search_term),
                func.lower(FacultyMember.department).like(search_term),
                func.lower(FacultyMember.designation).like(search_term)
            )
        )

    return query.offset(skip).limit(limit).all()

def update_faculty(db: Session, faculty_id: int, faculty_in: FacultyUpdate) -> Optional[FacultyMember]:
    db_faculty = get_faculty_by_id(db, faculty_id)
    if not db_faculty:
        return None

    update_data = faculty_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "email" and value:
            value = value.strip().lower()
        elif isinstance(value, str):
            value = value.strip()
        setattr(db_faculty, field, value)

    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def delete_faculty(db: Session, faculty_id: int) -> bool:
    db_faculty = get_faculty_by_id(db, faculty_id)
    if not db_faculty:
        return False
    db.delete(db_faculty)
    db.commit()
    return True
