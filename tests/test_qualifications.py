def test_add_multiple_qualifications(client):
    # 1. Create a single faculty member
    faculty_payload = {
        "first_name": "Ramesh",
        "last_name": "Kumar",
        "email": "ramesh.kumar@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 22
    }
    f_res = client.post("/api/v1/faculty", json=faculty_payload)
    assert f_res.status_code == 201
    faculty_id = f_res.json()["id"]

    # 2. Add B.Tech qualification
    q1 = {
        "degree": "B.Tech",
        "field_of_study": "Computer Science & Engineering",
        "institution": "IIT Madras",
        "passing_year": 1998
    }
    res1 = client.post(f"/api/v1/faculty/{faculty_id}/qualifications", json=q1)
    assert res1.status_code == 201
    assert res1.json()["degree"] == "B.Tech"

    # 3. Add M.Tech qualification
    q2 = {
        "degree": "M.Tech",
        "field_of_study": "Software Engineering",
        "institution": "IIT Bombay",
        "passing_year": 2000
    }
    res2 = client.post(f"/api/v1/faculty/{faculty_id}/qualifications", json=q2)
    assert res2.status_code == 201
    assert res2.json()["degree"] == "M.Tech"

    # 4. Add PhD qualification
    q3 = {
        "degree": "PhD",
        "field_of_study": "Artificial Intelligence",
        "institution": "IISc Bangalore",
        "passing_year": 2004
    }
    res3 = client.post(f"/api/v1/faculty/{faculty_id}/qualifications", json=q3)
    assert res3.status_code == 201
    assert res3.json()["degree"] == "PhD"

    # 5. Retrieve faculty member and verify all 3 qualifications exist under ONE faculty record
    faculty_check = client.get(f"/api/v1/faculty/{faculty_id}")
    assert faculty_check.status_code == 200
    f_data = faculty_check.json()
    assert len(f_data["qualifications"]) == 3
    degrees = [q["degree"] for q in f_data["qualifications"]]
    assert "B.Tech" in degrees
    assert "M.Tech" in degrees
    assert "PhD" in degrees

    # Verify no duplicate faculty records were created
    all_faculty = client.get("/api/v1/faculty")
    assert len(all_faculty.json()) == 1

def test_retrieve_all_qualifications(client):
    # Create 2 faculty members with qualifications
    f1 = client.post("/api/v1/faculty", json={
        "first_name": "Faculty",
        "last_name": "One",
        "email": "f1@university.edu",
        "department": "Civil Engineering",
        "designation": "Professor",
        "years_of_experience": 10,
        "qualifications": [{"degree": "B.Tech"}, {"degree": "M.Tech"}]
    })
    f2 = client.post("/api/v1/faculty", json={
        "first_name": "Faculty",
        "last_name": "Two",
        "email": "f2@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Lecturer",
        "years_of_experience": 2,
        "qualifications": [{"degree": "B.Tech"}, {"degree": "MBA"}]
    })
    assert f1.status_code == 201
    assert f2.status_code == 201

    quals_res = client.get("/api/v1/qualifications")
    assert quals_res.status_code == 200
    quals_list = quals_res.json()
    assert len(quals_list) == 4
