from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.qualification import FacultyQualification
from app.schemas.qualification import QualificationCreate

def add_qualification(db: Session, faculty_id: int, qual_in: QualificationCreate) -> FacultyQualification:
    db_qual = FacultyQualification(
        faculty_id=faculty_id,
        degree=qual_in.degree.strip(),
        field_of_study=qual_in.field_of_study.strip() if qual_in.field_of_study else None,
        institution=qual_in.institution.strip() if qual_in.institution else None,
        passing_year=qual_in.passing_year
    )
    db.add(db_qual)
    db.commit()
    db.refresh(db_qual)
    return db_qual

def get_qualification_by_id(db: Session, qualification_id: int) -> Optional[FacultyQualification]:
    return db.query(FacultyQualification).filter(FacultyQualification.id == qualification_id).first()

def get_qualifications_by_faculty_id(db: Session, faculty_id: int) -> List[FacultyQualification]:
    return db.query(FacultyQualification).filter(FacultyQualification.faculty_id == faculty_id).all()

def get_all_qualifications(db: Session, skip: int = 0, limit: int = 100) -> List[FacultyQualification]:
    return db.query(FacultyQualification).offset(skip).limit(limit).all()

def delete_qualification(db: Session, qualification_id: int) -> bool:
    qual = db.query(FacultyQualification).filter(FacultyQualification.id == qualification_id).first()
    if not qual:
        return False
    db.delete(qual)
    db.commit()
    return True
