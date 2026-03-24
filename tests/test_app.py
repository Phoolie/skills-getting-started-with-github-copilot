import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset de in-memory database vóór elke test
    for name, details in activities.items():
        if name == "Chess Club":
            details["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif name == "Programming Class":
            details["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif name == "Gym Class":
            details["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
        elif name == "Basketball Team":
            details["participants"] = ["alex@mergington.edu"]
        elif name == "Tennis Club":
            details["participants"] = ["sophia@mergington.edu"]
        elif name == "Art Studio":
            details["participants"] = ["isabella@mergington.edu", "liam@mergington.edu"]
        elif name == "Music Band":
            details["participants"] = ["lucas@mergington.edu"]
        else:
            details["participants"] = []

@pytest.fixture
def client():
    return TestClient(app)

def test_get_activities(client):
    # Arrange gebeurt via fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_participant(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_remove_participant(client):
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
