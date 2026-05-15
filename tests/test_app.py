import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def setup_function():
    # Reset activities to initial state before each test
    for activity in activities.values():
        if isinstance(activity["participants"], list):
            activity["participants"].clear()
    # Repopulate with initial participants
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Club"]["participants"] = ["liam@mergington.edu", "ava@mergington.edu"]
    activities["Basketball Team"]["participants"] = ["noah@mergington.edu", "mia@mergington.edu"]
    activities["Art Club"]["participants"] = ["isabella@mergington.edu", "lucas@mergington.edu"]
    activities["Drama Society"]["participants"] = ["amelia@mergington.edu", "henry@mergington.edu"]
    activities["Debate Team"]["participants"] = ["charlotte@mergington.edu", "jack@mergington.edu"]
    activities["Science Olympiad"]["participants"] = ["elijah@mergington.edu", "grace@mergington.edu"]

def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert response.json()["message"].startswith("Signed up")


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/Nonexistent/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# TODO: Add tests for unregister endpoint if implemented
