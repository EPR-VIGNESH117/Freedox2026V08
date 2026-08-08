from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class FacultyQualification(Base):
    __tablename__ = "faculty_qualifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    faculty_id = Column(Integer, ForeignKey("faculty_members.id", ondelete="CASCADE"), nullable=False, index=True)
    degree = Column(String(50), nullable=False, index=True)
    field_of_study = Column(String(100), nullable=True)
    institution = Column(String(150), nullable=True)
    passing_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    faculty = relationship("FacultyMember", back_populates="qualifications")
