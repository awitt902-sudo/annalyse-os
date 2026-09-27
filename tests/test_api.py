import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")

    # Import after environment variables are set so settings use the test database.
    from main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_login_and_protected_endpoint():
    from main import app

    client = TestClient(app)
    username = "pytest_user"
    password = "pytest_password_123"

    register = client.post("/api/v1/auth/register", json={"username": username, "password": password})
    assert register.status_code in (201, 400)

    token = client.post("/api/v1/auth/token", data={"username": username, "password": password})
    assert token.status_code == 200
    access_token = token.json()["access_token"]

    response = client.get("/api/v1/mission-control/dashboard", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "metrics" in response.json()
