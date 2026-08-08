from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.qualification import QualificationCreate, QualificationResponse

class FacultyBase(BaseModel):
    first_name: str = Field(..., example="Ramesh")
    last_name: str = Field(..., example="Kumar")
    email: EmailStr = Field(..., example="ramesh.kumar@example.edu")
    department: str = Field(..., example="Computer Science")
    designation: str = Field(..., example="Professor")
    years_of_experience: int = Field(0, ge=0, example=15)
    joining_date: Optional[date] = Field(None, example="2010-08-15")

class FacultyCreate(FacultyBase):
    qualifications: Optional[List[QualificationCreate]] = Field(default=[], description="List of initial qualifications")

class FacultyUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="Ramesh")
    last_name: Optional[str] = Field(None, example="Kumar")
    email: Optional[EmailStr] = Field(None, example="ramesh.kumar@example.edu")
    department: Optional[str] = Field(None, example="Computer Science")
    designation: Optional[str] = Field(None, example="Senior Professor")
    years_of_experience: Optional[int] = Field(None, ge=0, example=16)
    joining_date: Optional[date] = Field(None, example="2010-08-15")

class FacultyResponse(FacultyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    qualifications: List[QualificationResponse] = []

    model_config = ConfigDict(from_attributes=True)

class FacultyFilterParams(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    search: Optional[str] = None
