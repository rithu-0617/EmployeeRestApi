"""
Tests for /api/v1/auth endpoints.
"""


def test_register_success(client):
    resp = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "password": "Str0ngP@ss",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["user"]["username"] == "newuser"


def test_register_duplicate(client):
    payload = {"username": "dupuser", "password": "Str0ngP@ss"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_register_missing_fields(client):
    resp = client.post("/api/v1/auth/register", json={"username": ""})
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "password": "Str0ngP@ss",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "Str0ngP@ss",
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_password(client):
    client.post("/api/v1/auth/register", json={
        "username": "badpwuser",
        "password": "Str0ngP@ss",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "badpwuser",
        "password": "WrongPass",
    })
    assert resp.status_code == 401
