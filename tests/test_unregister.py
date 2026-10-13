def test_unregister_removes_participant_and_returns_updated_activities(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Unknown%20Activity/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_unregistered_participant(client):
    # Arrange
    activity = "Soccer Team"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Soccer%20Team/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_removes_all_duplicate_entries(client, activities_state):
    # Arrange
    activity = "Chess Club"
    email = "duplicate-student@mergington.edu"
    activities_state[activity]["participants"].extend([email, email])

    # Act
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities_state[activity]["participants"]
