import os

# Set testing DB environment variables before importing application modules
os.environ["ASYNC_DATABASE_URL"] = "sqlite+aiosqlite:///./ai_architect_test.db"
os.environ["DATABASE_URL"] = "sqlite:///./ai_architect_test.db"
os.environ["ENVIRONMENT"] = "testing"

import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    """
    Module-scoped Pytest fixture providing initialized TestClient inside active lifespan scope.
    """
    with TestClient(app) as test_client:
        yield test_client

def test_system_health(client):
    """
    Verifies that system status health router responds successfully.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_user_authentication_flow(client):
    """
    Verifies user registration, credential verification, and profile lookups.
    """
    email = "tester@enterprise.com"
    password = "testpassword123"
    
    # 1. Register User
    reg_response = client.post("/api/auth/register", json={
        "email": email,
        "full_name": "Test QA Engineer",
        "password": password,
        "role": "architect"
    })
    # Accept 201 Created or 400 Bad Request if user already exists from previous runs
    assert reg_response.status_code in (201, 400)
    
    # 2. Login User
    login_response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Retrieve User Profile (GET /api/auth/me)
    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == email
    assert me_data["full_name"] == "Test QA Engineer"

def test_project_recommendation_and_exports_flow(client):
    """
    Verifies project intake forms analysis, DB logging, details query, and ReportLab PDF downloads.
    """
    email = "tester@enterprise.com"
    password = "testpassword123"
    
    # Login to fetch headers
    login_res = client.post("/api/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. POST Analyze requirements
    project_payload = {
        "name": "Cloud Hospital ERP System",
        "description": "Multi-tenant Hospital Management System with HIPAA auditing.",
        "domain": "Healthcare",
        "expected_users": 15000,
        "budget": "50000 USD",
        "deadline": "4 months",
        "team_size": 6,
        "target_platform": "Web App",
        "required_features": "Billing, Scheduling, Electronic Health Records, HIPAA compliance Logs",
        "security_level": "Enterprise (Audited)",
        "scalability": "High",
        "availability": "99.99%",
        "preferred_cloud": "GCP",
        "expected_traffic": "Medium",
        "third_party_integrations": "Stripe, Twilio SMS"
    }
    
    analyze_res = client.post("/api/project/analyze", json=project_payload, headers=headers)
    assert analyze_res.status_code == 201
    analyze_data = analyze_res.json()
    assert "project_id" in analyze_data
    project_id = analyze_data["project_id"]
    
    # 2. GET Specific Recommendation details
    details_res = client.get(f"/api/project/{project_id}", headers=headers)
    assert details_res.status_code == 200
    details = details_res.json()
    assert details["project"]["name"] == "Cloud Hospital ERP System"
    assert "recommendation" in details
    assert "architecture_pattern" in details["recommendation"]
    
    # 3. GET History logs list
    history_res = client.get("/api/project/history", headers=headers)
    assert history_res.status_code == 200
    history = history_res.json()
    assert len(history) > 0
    assert any(h["project_id"] == project_id for h in history)
    
    # 4. GET Dynamic PDF Export download file
    pdf_res = client.get(f"/api/project/{project_id}/pdf", headers=headers)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000 # Verify PDF data size has loaded
