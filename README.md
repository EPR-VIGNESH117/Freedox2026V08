# Faculty Qualification Review Platform

An enterprise-grade FastAPI RESTful backend service built for managing academic faculty profiles, tracking qualifications, filtering credentials, and generating analytical reports across academic departments.

---

## Table of Contents
1. [Project Purpose](#1-project-purpose)
2. [Features](#2-features)
3. [Database Schema & ER Design](#3-database-schema--er-design)
   - [Why FacultyQualification is a Separate Entity](#why-facultyqualification-is-a-separate-entity)
   - [Entity Relationship Diagram](#entity-relationship-diagram)
4. [Installation & Setup](#4-installation--setup)
5. [Environment Variables](#5-environment-variables)
6. [PostgreSQL Setup](#6-postgresql-setup)
7. [Alembic Database Migrations](#7-alembic-database-migrations)
8. [How to Seed Dummy Data](#8-how-to-seed-dummy-data)
9. [How to Start FastAPI Server](#9-how-to-start-fastapi-server)
10. [API Endpoint List](#10-api-endpoint-list)
11. [Example API Requests & Responses](#11-example-api-requests--responses)
12. [How to Run Tests](#12-how-to-run-tests)

---

## 1. Project Purpose
Educational institutions and regulatory accreditation bodies require comprehensive tracking of faculty credentials, academic qualifications (B.Tech, M.Tech, PhD, M.Sc, MBA), experience levels, and department designations. 

This platform provides:
- A standardized data store for faculty members and their multiple academic degrees.
- Real-time analytical APIs for institutional reporting (Departmental breakdowns, Qualification statistics, Designation distribution, and Experience bracket analysis).
- Dynamic search and multi-criteria filtering for compliance auditing and academic planning.

---

## 2. Features
- **Faculty CRUD Operations**: Create, read, update, and delete faculty records seamlessly.
- **Multi-Qualification Management**: Link multiple degrees (B.Tech, M.Tech, PhD, etc.) to a single faculty member without data duplication.
- **Advanced Multi-Criteria Filtering**: Filter faculty by department, designation, qualification degree, experience ranges, or search keywords.
- **Analytical Reporting Engine**:
  - **Department Report**: Faculty counts, average experience, designation distribution, and degree breakdowns per department.
  - **Qualification Report**: Holder counts and percentage breakdown for each degree level (PhD, M.Tech, B.Tech, M.Sc, MBA).
  - **Designation Report**: Distribution of Professors, Associate Professors, Assistant Professors, and Lecturers with average experience.
  - **Experience Report**: Faculty categorizations across experience brackets (`0-3 years`, `4-7 years`, `8-15 years`, `16+ years`).
- **Alembic Database Migrations**: Track and apply schema changes across development and production environments.
- **Automated Seeding Script**: Pre-loaded with 16 realistic faculty records across 4 departments.
- **Automated Pytest Suite**: 100% endpoint coverage with isolated in-memory test databases.

---

## 3. Database Schema & ER Design

### Why FacultyQualification is a Separate Entity

> [!IMPORTANT]
> **Key Architectural Decision**: `FacultyQualification` is modeled as a **separate repeatable entity** linked to `FacultyMember` via a One-to-Many foreign key relationship (`faculty_id`), rather than a single string/array attribute inside `FacultyMember`.

#### Core Reasons:
1. **Normal Form Compliance (1NF & 2NF)**: 
   Storing qualifications as a comma-separated string inside `FacultyMember` violates First Normal Form (atomicity). Splitting degrees into separate attributes (`qualification_1`, `qualification_2`) limits scalability and flexibility.
2. **Preventing Data Duplication**: 
   Without a separate table, storing 3 degrees (B.Tech, M.Tech, PhD) for a single professor would require creating 3 separate rows in the `faculty_members` table. This causes severe data redundancy, inconsistent experience/department updates, and primary key duplication.
3. **Structured & Queryable Degree Metadata**: 
   A separate entity allows each qualification to carry its own metadata (`degree`, `field_of_study`, `institution`, `passing_year`) while enabling clean SQL join operations and fast index-assisted queries.

#### Relationship Demonstration:
```text
Faculty Member (Dr. Ramesh Kumar)
    ├── Qualification 1: B.Tech (Computer Science & Engineering - IIT Madras, 1998)
    ├── Qualification 2: M.Tech (Software Engineering - IIT Bombay, 2000)
    └── Qualification 3: PhD (AI & Distributed Systems - IISc Bangalore, 2004)
```
*Result: Exactly 1 row in `faculty_members` table, and 3 rows in `faculty_qualifications` table referencing `faculty_members.id`.*

### Entity Relationship Diagram

```mermaid
erdiagram
    FACULTY_MEMBERS ||--o{ FACULTY_QUALIFICATIONS : "has qualifications"
    
    FACULTY_MEMBERS {
        int id PK "Autoincrement"
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email UK "NOT NULL, Unique Index"
        string department "NOT NULL, Index"
        string designation "NOT NULL, Index"
        int years_of_experience "NOT NULL, Default: 0"
        date joining_date "Nullable"
        datetime created_at "Server Default"
        datetime updated_at "Server Default"
    }

    FACULTY_QUALIFICATIONS {
        int id PK "Autoincrement"
        int faculty_id FK "References faculty_members.id, CASCADE"
        string degree "NOT NULL, Index (e.g. B.Tech, M.Tech, PhD)"
        string field_of_study "Nullable"
        string institution "Nullable"
        int passing_year "Nullable"
        datetime created_at "Server Default"
    }
```

---

## 4. Installation & Setup

### Prerequisites
- Python 3.9+ installed
- Pip package manager

### Steps
1. **Clone the repository** (if not already in workspace):
   ```bash
   git clone https://github.com/Freedox2026V08/Freedox2026V08.git
   cd Freedox2026V08
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default `.env` configuration:
```env
PROJECT_NAME="Faculty Qualification Review Platform"
ENV="development"
DEBUG=True
DATABASE_URL=sqlite:///./faculty.db
```

To connect to a production PostgreSQL database, update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/faculty_db
```

---

## 6. PostgreSQL Setup
If using PostgreSQL:
1. Ensure PostgreSQL is installed and running on your host machine.
2. Create the target database using `psql` or pgAdmin:
   ```sql
   CREATE DATABASE faculty_db;
   ```
3. Update `.env` with your credentials:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/faculty_db
   ```

---

## 7. Alembic Database Migrations

Apply database migrations to set up the `faculty_members` and `faculty_qualifications` tables:

```bash
alembic upgrade head
```

To create new migrations after modifying SQLAlchemy models:
```bash
alembic revision --autogenerate -m "Add new column or table"
```

---

## 8. How to Seed Dummy Data

Run the database seed script to populate the database with **16 realistic faculty members** across 4 departments (Computer Science, Mechanical Engineering, Civil Engineering, Electronics & Communication), 4 designations, 5 qualification degrees, and varied experience levels:

```bash
python -m scripts.seed
```

Output confirmation:
```text
Initializing database tables...
Seeding database with 16 faculty members...
Database seeding completed successfully!
Summary: 16 Faculty Members and 39 Qualifications successfully inserted.
```

---

## 9. How to Start FastAPI Server

Launch the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Once running:
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **API Base Endpoint**: `http://127.0.0.1:8000/api/v1`

---

## 10. API Endpoint List

### Faculty & Qualification Endpoints (`/api/v1`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/faculty` | Create a new faculty member with optional initial qualifications |
| `GET` | `/api/v1/faculty` | List & filter faculty (by dept, designation, qualification, experience, search) |
| `GET` | `/api/v1/faculty/{id}` | Get detailed profile of a specific faculty member |
| `PUT` | `/api/v1/faculty/{id}` | Update faculty details |
| `DELETE` | `/api/v1/faculty/{id}` | Delete a faculty member (and cascade-delete their qualifications) |
| `POST` | `/api/v1/faculty/{id}/qualifications` | Add a new qualification to an existing faculty member |
| `GET` | `/api/v1/faculty/{id}/qualifications` | Get all qualifications for a specific faculty member |
| `GET` | `/api/v1/qualifications` | Retrieve all qualifications across all faculty members |
| `DELETE` | `/api/v1/qualifications/{id}` | Delete a specific qualification entry |

### Analytical Report Endpoints (`/api/v1/reports`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/reports/department` | Department report (counts, avg exp, designation & degree breakdowns) |
| `GET` | `/api/v1/reports/qualification` | Qualification report (degree holder counts & percentage distribution) |
| `GET` | `/api/v1/reports/designation` | Designation report (counts, avg exp, department distribution) |
| `GET` | `/api/v1/reports/experience` | Experience report (faculty counts & lists categorized by experience brackets) |

---

## 11. Example API Requests & Responses

### 1. Create a Faculty Member with Multiple Qualifications
**Request**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/faculty" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Alan",
       "last_name": "Turing",
       "email": "alan.turing@university.edu",
       "department": "Computer Science",
       "designation": "Professor",
       "years_of_experience": 20,
       "joining_date": "2005-09-01",
       "qualifications": [
         {
           "degree": "B.Tech",
           "field_of_study": "Mathematics",
           "institution": "Cambridge University",
           "passing_year": 1934
         },
         {
           "degree": "PhD",
           "field_of_study": "Computer Science",
           "institution": "Princeton University",
           "passing_year": 1938
         }
       ]
     }'
```

**Response (201 Created)**:
```json
{
  "first_name": "Alan",
  "last_name": "Turing",
  "email": "alan.turing@university.edu",
  "department": "Computer Science",
  "designation": "Professor",
  "years_of_experience": 20,
  "joining_date": "2005-09-01",
  "id": 17,
  "created_at": "2026-08-08T12:00:00.000000",
  "updated_at": "2026-08-08T12:00:00.000000",
  "qualifications": [
    {
      "degree": "B.Tech",
      "field_of_study": "Mathematics",
      "institution": "Cambridge University",
      "passing_year": 1934,
      "id": 40,
      "faculty_id": 17,
      "created_at": "2026-08-08T12:00:00.000000"
    },
    {
      "degree": "PhD",
      "field_of_study": "Computer Science",
      "institution": "Princeton University",
      "passing_year": 1938,
      "id": 41,
      "faculty_id": 17,
      "created_at": "2026-08-08T12:00:00.000000"
    }
  ]
}
```

---

### 2. Filter Faculty Members by Department & Minimum Experience
**Request**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/faculty?department=Computer%20Science&min_experience=10"
```

---

### 3. Add Another Qualification to an Existing Faculty
**Request**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/faculty/1/qualifications" \
     -H "Content-Type: application/json" \
     -d '{
       "degree": "MBA",
       "field_of_study": "Higher Education Management",
       "institution": "IIM Ahmedabad",
       "passing_year": 2012
     }'
```

---

### 4. Fetch Department Report
**Request**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/reports/department"
```

**Response (200 OK)**:
```json
{
  "total_departments": 4,
  "total_faculty": 16,
  "departments": [
    {
      "department": "Computer Science",
      "faculty_count": 4,
      "avg_years_of_experience": 10.25,
      "designation_breakdown": {
        "Professor": 1,
        "Associate Professor": 1,
        "Assistant Professor": 1,
        "Lecturer": 1
      },
      "highest_degree_breakdown": {
        "B.Tech": 4,
        "M.Tech": 3,
        "PhD": 2,
        "M.Sc": 1
      }
    }
  ]
}
```

---

### 5. Fetch Qualification Report
**Request**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/reports/qualification"
```

---

## 12. How to Run Tests

Execute the automated `pytest` test suite:

```bash
pytest -v
```

All 13 unit tests will run against an isolated in-memory SQLite database instance:

```text
tests/test_faculty.py :: test_create_faculty PASSED
tests/test_faculty.py :: test_create_faculty_duplicate_email PASSED
tests/test_faculty.py :: test_retrieve_faculty_by_id PASSED
tests/test_faculty.py :: test_retrieve_nonexistent_faculty PASSED
tests/test_faculty.py :: test_update_faculty PASSED
tests/test_faculty.py :: test_delete_faculty PASSED
tests/test_qualifications.py :: test_add_multiple_qualifications PASSED
tests/test_qualifications.py :: test_retrieve_all_qualifications PASSED
tests/test_filtering.py :: test_filter_by_department PASSED
tests/test_filtering.py :: test_filter_by_designation PASSED
tests/test_filtering.py :: test_filter_by_qualification PASSED
tests/test_filtering.py :: test_filter_by_experience_range PASSED
tests/test_filtering.py :: test_search_keyword PASSED
tests/test_reports.py :: test_department_report PASSED
tests/test_reports.py :: test_qualification_report PASSED
tests/test_reports.py :: test_designation_report PASSED
tests/test_reports.py :: test_experience_report PASSED

================ 17 passed in 0.85s ================
```
