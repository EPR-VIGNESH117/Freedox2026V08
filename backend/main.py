from typing import Optional
from fastapi import FastAPI, Depends,HTTPException,status
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Faculty Model
class Faculty(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    department: str
    designation: str
    qualification: str
    specialization: str
    joining_date: str
    experience_years: int

# 2. Database Connection
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

# 3. Seed 20 Faculty Records
initial_faculty_data = [
    Faculty(id="FAC001", name="Dr. Rajesh Sharma", department="Computer Science & Eng.", designation="Professor & Head", qualification="Ph.D. (IIT Bombay)", specialization="Machine Learning & AI", joining_date="2010-07-15", experience_years=18),
    Faculty(id="FAC002", name="Dr. Ananya Sen", department="Computer Science & Eng.", designation="Associate Professor", qualification="Ph.D. (IISc Bangalore)", specialization="Cyber Security & Cryptography", joining_date="2015-08-10", experience_years=12),
    Faculty(id="FAC003", name="Mr. Vikramaditya Rao", department="Computer Science & Eng.", designation="Assistant Professor", qualification="M.Tech (NIT Surathkal)", specialization="Cloud Computing & DevOps", joining_date="2020-02-01", experience_years=6),
    Faculty(id="FAC004", name="Dr. Meera Kulkarni", department="Information Science", designation="Associate Professor", qualification="Ph.D. (VTU)", specialization="Data Mining & Big Data Analytics", joining_date="2016-01-18", experience_years=11),
    Faculty(id="FAC005", name="Ms. Priya Nair", department="Information Science", designation="Assistant Professor", qualification="M.Tech (BMSCE)", specialization="Web Technologies & UI/UX", joining_date="2021-08-05", experience_years=4),
    Faculty(id="FAC006", name="Dr. Suresh Menon", department="Electronics & Comm.", designation="Professor", qualification="Ph.D. (IIT Madras)", specialization="VLSI Design & Embedded Systems", joining_date="2008-06-01", experience_years=20),
    Faculty(id="FAC007", name="Dr. Kavita Reddy", department="Electronics & Comm.", designation="Associate Professor", qualification="Ph.D. (NIT Trichy)", specialization="Signal Processing & Digital Comm.", joining_date="2014-09-12", experience_years=13),
    Faculty(id="FAC008", name="Mr. Amit Verma", department="Mechanical Eng.", designation="Assistant Professor", qualification="M.Tech (IIT Kharagpur)", specialization="Thermal Engineering & Robotics", joining_date="2019-07-15", experience_years=7),
    Faculty(id="FAC009", name="Dr. Ramesh Bhat", department="Mechanical Eng.", designation="Professor & Dean", qualification="Ph.D. (IISc Bangalore)", specialization="Fluid Mechanics & Aerodynamics", joining_date="2005-01-10", experience_years=24),
    Faculty(id="FAC010", name="Dr. Sunita Deshmukh", department="Civil Engineering", designation="Associate Professor", qualification="Ph.D. (IIT Delhi)", specialization="Structural Engineering & Concrete Tech", joining_date="2013-08-20", experience_years=14),
    Faculty(id="FAC011", name="Mr. Arvind Swamy", department="Civil Engineering", designation="Assistant Professor", qualification="M.E. (BITS Pilani)", specialization="Environmental Eng. & Hydrology", joining_date="2022-02-01", experience_years=3),
    Faculty(id="FAC012", name="Dr. Sanjay Gupta", department="Electrical Engineering", designation="Professor", qualification="Ph.D. (IIT Roorkee)", specialization="Power Systems & Renewable Energy", joining_date="2009-11-11", experience_years=19),
    Faculty(id="FAC013", name="Dr. Deepa Patil", department="Electrical Engineering", designation="Assistant Professor", qualification="Ph.D. (NIT Calicut)", specialization="Control Systems & Smart Grids", joining_date="2018-08-15", experience_years=8),
    Faculty(id="FAC014", name="Dr. Harish Chandra", department="Mathematics", designation="Professor", qualification="Ph.D. (University of Delhi)", specialization="Applied Linear Algebra & Optimization", joining_date="2007-07-01", experience_years=22),
    Faculty(id="FAC015", name="Dr. Pooja Hegde", department="Mathematics", designation="Assistant Professor", qualification="Ph.D. (IIT Kanpur)", specialization="Graph Theory & Numerical Analysis", joining_date="2021-01-10", experience_years=5),
    Faculty(id="FAC016", name="Dr. Robert D'Souza", department="Physics", designation="Associate Professor", qualification="Ph.D. (TIFR Mumbai)", specialization="Quantum Mechanics & Materials", joining_date="2012-09-05", experience_years=15),
    Faculty(id="FAC017", name="Dr. Archana Joshi", department="Chemistry", designation="Associate Professor", qualification="Ph.D. (University of Hyderabad)", specialization="Organic Synthesis & Polymers", joining_date="2014-08-14", experience_years=13),
    Faculty(id="FAC018", name="Dr. Nitin Saxena", department="Humanities & Management", designation="Professor", qualification="Ph.D. (IIM Ahmedabad)", specialization="Organizational Behavior & Ethics", joining_date="2011-08-01", experience_years=17),
    Faculty(id="FAC019", name="Ms. Neha Joshi", department="Humanities & Management", designation="Assistant Professor", qualification="MBA (XIMB)", specialization="Finance & Corporate Strategy", joining_date="2020-01-15", experience_years=6),
    Faculty(id="FAC020", name="Dr. Shalini Prasad", department="Biotechnology", designation="Associate Professor", qualification="Ph.D. (JNCASR)", specialization="Genetic Engineering & Bioinformatics", joining_date="2017-03-01", experience_years=10),
]

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Only seed if database is empty
        existing = session.exec(select(Faculty)).first()
        if not existing:
            for fac in initial_faculty_data:
                session.add(fac)
            session.commit()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

def get_session():
    with Session(engine) as session:
        yield session

# 4. API Endpoints

# GET all faculty members
@app.get("/faculty/", response_model=list[Faculty])
def get_all_faculty(session: Session = Depends(get_session)):
    return session.exec(select(Faculty)).all()

# GET single faculty member by ID
@app.get("/faculty/{faculty_id}", response_model=Faculty)
def get_faculty_by_id(faculty_id: str, session: Session = Depends(get_session)):
    faculty = session.get(Faculty, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    return faculty

@app.post("/faculty/", response_model=Faculty, status_code=status.HTTP_201_CREATED)
def create_faculty(faculty: Faculty, session: Session = Depends(get_session)):
    session.add(faculty)
    session.commit()
    session.refresh(faculty)
    return faculty 