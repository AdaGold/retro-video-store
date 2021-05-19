from app.models.video import Video

def test_add_video(client):
    # Act
    response = client.post("/videos", json={
        "title": "Howls Moving Castle",
        "release_date":"2005-07-17",
        "total_inventory":10,
        "current_inventory":10
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201