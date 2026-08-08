from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class FacultyMember(Base):
    __tablename__ = "faculty_members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(100), index=True, nullable=False)
    designation = Column(String(100), index=True, nullable=False)
    years_of_experience = Column(Integer, nullable=False, default=0)
    joining_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to repeatable FacultyQualification entity
    qualifications = relationship(
        "FacultyQualification",
        back_populates="faculty",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
