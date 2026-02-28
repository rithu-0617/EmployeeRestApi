"""
Shared test fixtures.
"""
import os
import shutil
import pytest
from app import create_app


@pytest.fixture(scope="session", autouse=True)
def _clean_test_data():
    """Remove test data directory after the full test suite."""
    yield
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


@pytest.fixture()
def app():
    application = create_app("testing")
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    """Register + login and return Authorization header dict."""
    client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "password": "TestPass123!",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "TestPass123!",
    })
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
