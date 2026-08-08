import pytest

@pytest.fixture
def seeded_client(client):
    # Seed 3 faculty members with different attributes
    f1 = {
        "first_name": "Ramesh",
        "last_name": "Kumar",
        "email": "ramesh.kumar@university.edu",
        "department": "Computer Science",
        "designation": "Professor",
        "years_of_experience": 20,
        "qualifications": [{"degree": "PhD"}]
    }
    f2 = {
        "first_name": "Anita",
        "last_name": "Sharma",
        "email": "anita.sharma@university.edu",
        "department": "Mechanical Engineering",
        "designation": "Associate Professor",
        "years_of_experience": 10,
        "qualifications": [{"degree": "M.Tech"}]
    }
    f3 = {
        "first_name": "Suresh",
        "last_name": "Patel",
        "email": "suresh.patel@university.edu",
        "department": "Computer Science",
        "designation": "Assistant Professor",
        "years_of_experience": 3,
        "qualifications": [{"degree": "B.Tech"}]
    }
    client.post("/api/v1/faculty", json=f1)
    client.post("/api/v1/faculty", json=f2)
    client.post("/api/v1/faculty", json=f3)
    return client

def test_filter_by_department(seeded_client):
    res = seeded_client.get("/api/v1/faculty?department=Computer Science")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    for f in data:
        assert f["department"] == "Computer Science"

def test_filter_by_designation(seeded_client):
    res = seeded_client.get("/api/v1/faculty?designation=Professor")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Ramesh"

def test_filter_by_qualification(seeded_client):
    res = seeded_client.get("/api/v1/faculty?qualification=PhD")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Ramesh"

def test_filter_by_experience_range(seeded_client):
    res = seeded_client.get("/api/v1/faculty?min_experience=5&max_experience=15")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Anita"

def test_search_keyword(seeded_client):
    res = seeded_client.get("/api/v1/faculty?search=Patel")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["last_name"] == "Patel"
