from flask.wrappers import Response
from app.models.customer import Customer


def test_create_customer(client):
    # Act
    response = client.post("/customers", json={
        "name": "Lars Sankar",
        "postal_code": "75007",
        "phone": "111-111-1111"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201

def test_get_customers(client, two_customers):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == "minh"
    assert response_body[0]["postal_code"] == "98123"
    assert response_body[0]["videos_checked_out_count"] == 0
    assert response_body[0]["phone"] == "555-555-5555"

    assert response_body[1]["name"] == "summer"
    assert response_body[1]["postal_code"] == "98123"
    assert response_body[1]["videos_checked_out_count"] == 0
    assert response_body[1]["phone"] == "444-444-4444"


def test_get_customer_no_saved_customers(client):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_customer_by_id(client, one_customer):
    #Act
    response = client.get("/customers/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body["name"] == "minh"
    assert response_body["postal_code"] == "98123"
    assert response_body["videos_checked_out_count"] == 0
    assert response_body["phone"] == "555-555-5555"
    assert response_body["id"] == 1

def test_update_customer(client, one_customer):
    #Act
    response = client.put("/customers/1", json={
        "name": "Updated Customer name",
        "postal_code": "Updated postal code",
        "phone": "Updated phone number"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body["name"] == "Updated Customer name"
    assert response_body["postal_code"] == "Updated postal code"
    assert response_body["videos_checked_out_count"] == 0
    assert response_body["phone"] == "Updated phone number"
    assert response_body["id"] == 1
    
