"""Tests for the rules engine API."""

from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_eligible_low_income():
    response = client.post(
        "/evaluate/benefit-eligibility",
        json={"age": 30, "income": 12000, "is_resident": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is True
    assert data["monthly_amount"] == 500.0


def test_eligible_mid_income():
    response = client.post(
        "/evaluate/benefit-eligibility",
        json={"age": 40, "income": 20000, "is_resident": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is True
    assert data["monthly_amount"] == 300.0


def test_ineligible_underage():
    response = client.post(
        "/evaluate/benefit-eligibility",
        json={"age": 16, "income": 10000, "is_resident": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is False
    assert data["monthly_amount"] == 0.0


def test_ineligible_high_income():
    response = client.post(
        "/evaluate/benefit-eligibility",
        json={"age": 25, "income": 35000, "is_resident": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is False
    assert data["monthly_amount"] == 0.0


def test_ineligible_non_resident():
    response = client.post(
        "/evaluate/benefit-eligibility",
        json={"age": 30, "income": 12000, "is_resident": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is False
    assert data["monthly_amount"] == 0.0
