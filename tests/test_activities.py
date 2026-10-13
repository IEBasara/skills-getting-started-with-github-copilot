def test_get_activities_returns_activity_details(client, activities_state):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities_state
    assert response.json()[expected_activity]["max_participants"] == 12
