import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (client is already arranged)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Clean up in case user is already signed up
    client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_prevent_duplicate_signup():
    # Arrange
    email = "dupeuser@mergington.edu"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/signup?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

# Add more tests as needed for DELETE and edge cases
