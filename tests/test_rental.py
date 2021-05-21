from app.models.rental import Rental

def test_create_rental(client, one_customer, one_video):
    # Act
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["customer_id"] == 1
    assert response_body["video_id"] == 1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 9

def test_create_rental_invalid_customer_id(client, one_video):
    # Act
    response = client.post("/rentals/check-out", json={
        "customer_id": 1000, 
        "video_id": 1
    })

    #Assert
    assert response.status_code == 404

def test_create_rental_customer_id_not_int(client, one_video):
    # Act
    response = client.post("/rentals/check-out", json={
        "customer_id": "Not an Int", 
        "video_id": 1
    })

    #Assert
    assert response.status_code == 400

def test_return_rental(client, one_rental):
    # Act
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body["customer_id"] == 1
    assert response_body["video_id"] == 1
    assert response_body["videos_checked_out_count"] == 0
    assert response_body["available_inventory"] == 10

def test_return_rental_has_no_video_id(client, one_rental):
    # Act
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1000
    })

    #Assert
    assert response.status_code == 400