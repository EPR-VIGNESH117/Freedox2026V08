import pytest

@pytest.fixture
def report_client(client):
    f1 = {
        "first_name": "Ramesh",
        "last_name": "Kumar",
        "email": "ramesh.kumar@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 20,
        "qualifications": [{"degree": "B.Tech"}, {"degree": "M.Tech"}, {"degree": "PhD"}]
    }
    f2 = {
        "first_name": "Anita",
        "last_name": "Sharma",
        "email": "anita.sharma@university.edu",
        "department": "Computer Science",
        "designation": "Associate Professor",
        "years_of_experience": 10,
        "qualifications": [{"degree": "B.Tech"}, {"degree": "PhD"}]
    }
    f3 = {
        "first_name": "Vikram",
        "last_name": "Singh",
        "email": "vikram.singh@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Assistant Professor",
        "years_of_experience": 5,
        "qualifications": [{"degree": "B.Tech"}, {"degree": "M.Tech"}]
    }
    client.post("/api/v1/faculty", json=f1)
    client.post("/api/v1/faculty", json=f2)
    client.post("/api/v1/faculty", json=f3)
    return client

def test_department_report(report_client):
    res = report_client.get("/api/v1/reports/department")
    assert res.status_code == 200
    data = res.json()
    assert data["total_faculty"] == 3
    assert data["total_departments"] == 2
    
    # Check CS department metrics
    cs_dept = next(d for d in data["departments"] if d["department"] == "Computer Science")
    assert cs_dept["faculty_count"] == 2
    assert cs_dept["avg_years_of_experience"] == 15.0  # (20+10)/2
    assert cs_dept["designation_breakdown"]["Professor"] == 1
    assert cs_dept["designation_breakdown"]["Associate Professor"] == 1

def test_qualification_report(report_client):
    res = report_client.get("/api/v1/reports/qualification")
    assert res.status_code == 200
    data = res.json()
    assert data["total_faculty"] == 3
    assert data["total_qualifications_recorded"] == 7
    
    # Check degree counts
    breakdown = {q["degree"]: q["total_holders"] for q in data["qualifications_breakdown"]}
    assert breakdown["B.Tech"] == 3
    assert breakdown["M.Tech"] == 2
    assert breakdown["PhD"] == 2

def test_designation_report(report_client):
    res = report_client.get("/api/v1/reports/designation")
    assert res.status_code == 200
    data = res.json()
    assert data["total_faculty"] == 3
    designations = {d["designation"]: d for d in data["designations"]}
    assert "Professor" in designations
    assert designations["Professor"]["faculty_count"] == 1
    assert designations["Professor"]["avg_years_of_experience"] == 20.0

def test_experience_report(report_client):
    res = report_client.get("/api/v1/reports/experience")
    assert res.status_code == 200
    data = res.json()
    assert data["total_faculty"] == 3
    assert data["overall_avg_experience"] == round((20 + 10 + 5) / 3, 2)
    assert len(data["brackets"]) == 4
