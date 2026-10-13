def test_signup_adds_participant_and_returns_it_in_activities(client):
    # Arrange
    activity = "Soccer Team"
    email = "new-student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Soccer%20Team/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities_response.json()[activity]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    email = "new-student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client, activities_state):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities_state[activity]["participants"].copy()

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities_state[activity]["participants"] == original_participants
