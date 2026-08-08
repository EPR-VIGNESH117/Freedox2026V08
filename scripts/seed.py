import sys
import os
from datetime import date

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.faculty import FacultyMember
from app.models.qualification import FacultyQualification

SEED_FACULTY_DATA = [
    {
        "first_name": "Ramesh",
        "last_name": "Kumar",
        "email": "ramesh.kumar@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 22,
        "joining_date": date(2004, 7, 15),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Computer Science & Engineering", "institution": "IIT Madras", "passing_year": 1998},
            {"degree": "M.Tech", "field_of_study": "Software Engineering", "institution": "IIT Bombay", "passing_year": 2000},
            {"degree": "PhD", "field_of_study": "Artificial Intelligence & Distributed Systems", "institution": "IISc Bangalore", "passing_year": 2004}
        ]
    },
    {
        "first_name": "Anita",
        "last_name": "Sharma",
        "email": "anita.sharma@university.edu",
        "department": "Computer Science",
        "designation": "Associate Professor",
        "years_of_experience": 12,
        "joining_date": date(2014, 6, 10),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Information Technology", "institution": "Anna University", "passing_year": 2008},
            {"degree": "M.Tech", "field_of_study": "Computer Networks", "institution": "NIT Trichy", "passing_year": 2010},
            {"degree": "PhD", "field_of_study": "Cybersecurity & Cryptography", "institution": "IIT Delhi", "passing_year": 2014}
        ]
    },
    {
        "first_name": "Suresh",
        "last_name": "Patel",
        "email": "suresh.patel@university.edu",
        "department": "Computer Science",
        "designation": "Assistant Professor",
        "years_of_experience": 5,
        "joining_date": date(2021, 8, 1),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Computer Science", "institution": "Gujarat Technological University", "passing_year": 2017},
            {"degree": "M.Tech", "field_of_study": "Data Science & Cloud Computing", "institution": "IIT Kharagpur", "passing_year": 2019}
        ]
    },
    {
        "first_name": "Meera",
        "last_name": "Deshmukh",
        "email": "meera.deshmukh@university.edu",
        "department": "Computer Science",
        "designation": "Lecturer",
        "years_of_experience": 2,
        "joining_date": date(2024, 1, 15),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Computer Engineering", "institution": "Pune University", "passing_year": 2021},
            {"degree": "M.Sc", "field_of_study": "Computer Science", "institution": "BITS Pilani", "passing_year": 2023}
        ]
    },
    {
        "first_name": "Vikram",
        "last_name": "Singh",
        "email": "vikram.singh@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Professor",
        "years_of_experience": 19,
        "joining_date": date(2007, 3, 20),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Mechanical Engineering", "institution": "IIT Roorkee", "passing_year": 2001},
            {"degree": "M.Tech", "field_of_study": "Thermal & Energy Systems", "institution": "IIT Kanpur", "passing_year": 2003},
            {"degree": "PhD", "field_of_study": "Computational Fluid Dynamics", "institution": "IIT Madras", "passing_year": 2007}
        ]
    },
    {
        "first_name": "Priya",
        "last_name": "Nair",
        "email": "priya.nair@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Associate Professor",
        "years_of_experience": 11,
        "joining_date": date(2015, 9, 5),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Automobile Engineering", "institution": "Kerala University", "passing_year": 2009},
            {"degree": "M.Tech", "field_of_study": "Manufacturing Technology", "institution": "NIT Calicut", "passing_year": 2011},
            {"degree": "PhD", "field_of_study": "Robotics & Automation", "institution": "IIT Bombay", "passing_year": 2015}
        ]
    },
    {
        "first_name": "Arjun",
        "last_name": "Reddy",
        "email": "arjun.reddy@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Assistant Professor",
        "years_of_experience": 6,
        "joining_date": date(2020, 7, 1),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Mechanical Engineering", "institution": "JNTU Hyderabad", "passing_year": 2016},
            {"degree": "M.Tech", "field_of_study": "CAD/CAM & Mechatronics", "institution": "IIT Hyderabad", "passing_year": 2018}
        ]
    },
    {
        "first_name": "Kavita",
        "last_name": "Joshi",
        "email": "kavita.joshi@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Lecturer",
        "years_of_experience": 3,
        "joining_date": date(2023, 2, 10),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Industrial Production", "institution": "VTU Belagavi", "passing_year": 2020},
            {"degree": "MBA", "field_of_study": "Operations & Supply Chain", "institution": "IIM Ahmedabad", "passing_year": 2022}
        ]
    },
    {
        "first_name": "Rajesh",
        "last_name": "Verma",
        "email": "rajesh.verma@university.edu",
        "department": "Civil Engineering",
        "designation": "Professor",
        "years_of_experience": 18,
        "joining_date": date(2008, 8, 12),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Civil Engineering", "institution": "IIT BHU Varanasi", "passing_year": 2002},
            {"degree": "M.Tech", "field_of_study": "Structural Engineering", "institution": "IIT Roorkee", "passing_year": 2004},
            {"degree": "PhD", "field_of_study": "Earthquake Resistant Structures", "institution": "IIT Delhi", "passing_year": 2008}
        ]
    },
    {
        "first_name": "Sunita",
        "last_name": "Rao",
        "email": "sunita.rao@university.edu",
        "department": "Civil Engineering",
        "designation": "Associate Professor",
        "years_of_experience": 10,
        "joining_date": date(2016, 5, 20),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Civil Engineering", "institution": "Osmania University", "passing_year": 2010},
            {"degree": "M.Tech", "field_of_study": "Environmental Engineering", "institution": "IIT Kharagpur", "passing_year": 2012},
            {"degree": "PhD", "field_of_study": "Water Resource Systems", "institution": "IISc Bangalore", "passing_year": 2016}
        ]
    },
    {
        "first_name": "Deepak",
        "last_name": "Gupta",
        "email": "deepak.gupta@university.edu",
        "department": "Civil Engineering",
        "designation": "Assistant Professor",
        "years_of_experience": 4,
        "joining_date": date(2022, 9, 1),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Infrastructure Engineering", "institution": "SRM Institute", "passing_year": 2018},
            {"degree": "M.Tech", "field_of_study": "Geotechnical Engineering", "institution": "IIT Guwahati", "passing_year": 2020}
        ]
    },
    {
        "first_name": "Pooja",
        "last_name": "Banerjee",
        "email": "pooja.banerjee@university.edu",
        "department": "Civil Engineering",
        "designation": "Lecturer",
        "years_of_experience": 1,
        "joining_date": date(2025, 6, 1),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Civil Engineering", "institution": "Jadavpur University", "passing_year": 2023},
            {"degree": "M.Sc", "field_of_study": "Urban Planning & Remote Sensing", "institution": "IIRS Dehradun", "passing_year": 2025}
        ]
    },
    {
        "first_name": "Sanjay",
        "last_name": "Kulkarni",
        "email": "sanjay.kulkarni@university.edu",
        "department": "Electronics & Communication",
        "designation": "Professor",
        "years_of_experience": 20,
        "joining_date": date(2006, 1, 10),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Electronics & Communication", "institution": "IIT Madras", "passing_year": 2000},
            {"degree": "M.Tech", "field_of_study": "VLSI Design & Embedded Systems", "institution": "IIT Bombay", "passing_year": 2002},
            {"degree": "PhD", "field_of_study": "Nano-Electronics & Photonics", "institution": "IISc Bangalore", "passing_year": 2006}
        ]
    },
    {
        "first_name": "Sneha",
        "last_name": "Menon",
        "email": "sneha.menon@university.edu",
        "department": "Electronics & Communication",
        "designation": "Associate Professor",
        "years_of_experience": 9,
        "joining_date": date(2017, 10, 12),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "Electronics & Telecommunication", "institution": "CUSAT Kochi", "passing_year": 2011},
            {"degree": "M.Tech", "field_of_study": "Signal Processing", "institution": "NIT Trichy", "passing_year": 2013},
            {"degree": "PhD", "field_of_study": "5G Wireless Networks", "institution": "IIT Madras", "passing_year": 2017}
        ]
    },
    {
        "first_name": "Alok",
        "last_name": "Mishra",
        "email": "alok.mishra@university.edu",
        "department": "Electronics & Communication",
        "designation": "Assistant Professor",
        "years_of_experience": 7,
        "joining_date": date(2019, 4, 15),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "ECE", "institution": "AKTU Lucknow", "passing_year": 2015},
            {"degree": "M.Tech", "field_of_study": "Micro-Electronics", "institution": "IIT BHU", "passing_year": 2017}
        ]
    },
    {
        "first_name": "Divya",
        "last_name": "Saxena",
        "email": "divya.saxena@university.edu",
        "department": "Electronics & Communication",
        "designation": "Lecturer",
        "years_of_experience": 3,
        "joining_date": date(2023, 7, 1),
        "qualifications": [
            {"degree": "B.Tech", "field_of_study": "ECE", "institution": "Amity University", "passing_year": 2021},
            {"degree": "MBA", "field_of_study": "Technology Management", "institution": "NMIMS Mumbai", "passing_year": 2023}
        ]
    }
]

def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_count = db.query(FacultyMember).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} faculty members. Clearing existing data for fresh seed...")
            db.query(FacultyQualification).delete()
            db.query(FacultyMember).delete()
            db.commit()

        print(f"Seeding database with {len(SEED_FACULTY_DATA)} faculty members...")
        for faculty_data in SEED_FACULTY_DATA:
            quals_data = faculty_data.pop("qualifications", [])
            faculty = FacultyMember(**faculty_data)
            db.add(faculty)
            db.flush()

            for q_data in quals_data:
                qual = FacultyQualification(
                    faculty_id=faculty.id,
                    degree=q_data["degree"],
                    field_of_study=q_data.get("field_of_study"),
                    institution=q_data.get("institution"),
                    passing_year=q_data.get("passing_year")
                )
                db.add(qual)

        db.commit()
        print("Database seeding completed successfully!")
        
        total_faculty = db.query(FacultyMember).count()
        total_quals = db.query(FacultyQualification).count()
        print(f"Summary: {total_faculty} Faculty Members and {total_quals} Qualifications successfully inserted.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
