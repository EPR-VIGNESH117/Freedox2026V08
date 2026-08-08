def test_create_faculty(client):
    payload = {
        "first_name": "Alan",
        "last_name": "Turing",
        "email": "alan.turing@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 20,
        "joining_date": "2005-09-01",
        "qualifications": [
            {
                "degree": "PhD",
                "field_of_study": "Mathematics & Computing",
                "institution": "Cambridge University",
                "passing_year": 1938
            }
        ]
    }
    response = client.post("/api/v1/faculty", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["first_name"] == "Alan"
    assert data["email"] == "alan.turing@university.edu"
    assert len(data["qualifications"]) == 1
    assert data["qualifications"][0]["degree"] == "PhD"

def test_create_faculty_duplicate_email(client):
    payload = {
        "first_name": "Grace",
        "last_name": "Hopper",
        "email": "grace.hopper@university.edu",
        "department": "Computer Science",
        "designation": "Associate Professor",
        "years_of_experience": 15
    }
    r1 = client.post("/api/v1/faculty", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/v1/faculty", json=payload)
    assert r2.status_code == 400
    assert "already exists" in r2.json()["detail"]

def test_retrieve_faculty_by_id(client):
    payload = {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email": "ada.lovelace@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 12
    }
    create_res = client.post("/api/v1/faculty", json=payload)
    faculty_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/faculty/{faculty_id}")
    assert get_res.status_code == 200
    assert get_res.json()["first_name"] == "Ada"

def test_retrieve_nonexistent_faculty(client):
    get_res = client.get("/api/v1/faculty/9999")
    assert get_res.status_code == 404

def test_update_faculty(client):
    payload = {
        "first_name": "Nikola",
        "last_name": "Tesla",
        "email": "nikola.tesla@university.edu",
        "department": "Electronics & Communication",
        "designation": "Assistant Professor",
        "years_of_experience": 5
    }
    create_res = client.post("/api/v1/faculty", json=payload)
    faculty_id = create_res.json()["id"]

    update_payload = {
        "designation": "Associate Professor",
        "years_of_experience": 8
    }
    update_res = client.put(f"/api/v1/faculty/{faculty_id}", json=update_payload)
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["designation"] == "Associate Professor"
    assert data["years_of_experience"] == 8
    assert data["first_name"] == "Nikola"

def test_delete_faculty(client):
    payload = {
        "first_name": "Thomas",
        "last_name": "Edison",
        "email": "thomas.edison@university.edu",
        "department": "Electronics & Communication",
        "designation": "Lecturer",
        "years_of_experience": 3
    }
    create_res = client.post("/api/v1/faculty", json=payload)
    faculty_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/faculty/{faculty_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/api/v1/faculty/{faculty_id}")
    assert get_res.status_code == 404
