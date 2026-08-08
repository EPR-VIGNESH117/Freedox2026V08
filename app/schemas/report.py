from typing import List, Dict, Any
from pydantic import BaseModel

class DepartmentReportItem(BaseModel):
    department: str
    faculty_count: int
    avg_years_of_experience: float
    designation_breakdown: Dict[str, int]
    highest_degree_breakdown: Dict[str, int]

class DepartmentReportResponse(BaseModel):
    total_departments: int
    total_faculty: int
    departments: List[DepartmentReportItem]

class QualificationReportItem(BaseModel):
    degree: str
    total_holders: int
    percentage_of_faculty: float

class QualificationReportResponse(BaseModel):
    total_faculty: int
    total_qualifications_recorded: int
    qualifications_breakdown: List[QualificationReportItem]

class DesignationReportItem(BaseModel):
    designation: str
    faculty_count: int
    avg_years_of_experience: float
    department_distribution: Dict[str, int]

class DesignationReportResponse(BaseModel):
    total_faculty: int
    designations: List[DesignationReportItem]

class ExperienceBracketItem(BaseModel):
    bracket: str
    min_years: int
    max_years: float  # float('inf') handled or high number
    faculty_count: int
    avg_years_of_experience: float
    faculty_list: List[Dict[str, Any]]

class ExperienceReportResponse(BaseModel):
    total_faculty: int
    overall_avg_experience: float
    brackets: List[ExperienceBracketItem]
