"""
Tests for /api/v1/health endpoint.
"""


def test_health_returns_200(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"
