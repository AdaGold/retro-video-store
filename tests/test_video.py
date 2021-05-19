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


def test_get_video_no_saved_videos(client):
    # Act
    response = client.get("/videos")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_customers(client, two_videos):
    # Act
    response = client.get("/videos")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

    assert response_body[0]["title"] == "Howls Moving Castle"
    assert response_body[0]["total_inventory"] == 10
    assert response_body[0]["available_inventory"] == 10

    assert response_body[1]["title"] == "10 Things I Hate About You"
    assert response_body[1]["total_inventory"] == 3
    assert response_body[1]["available_inventory"] == 3


def test_get_customer_by_id(client, one_video):
    #Act
    response = client.get("/videos/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["title"] == "Howls Moving Castle"
    assert response_body["total_inventory"] == 10
    assert response_body["available_inventory"] == 10