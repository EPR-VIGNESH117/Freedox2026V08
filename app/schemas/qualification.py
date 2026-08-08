from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class QualificationBase(BaseModel):
    degree: str = Field(..., example="PhD", description="Degree or certification name, e.g., B.Tech, M.Tech, PhD, M.Sc, MBA")
    field_of_study: Optional[str] = Field(None, example="Computer Science & Engineering", description="Specialization field")
    institution: Optional[str] = Field(None, example="IIT Madras", description="Granting institution")
    passing_year: Optional[int] = Field(None, example=2018, description="Year qualification was awarded")

class QualificationCreate(QualificationBase):
    pass

class QualificationResponse(QualificationBase):
    id: int
    faculty_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
