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

def test_get_customer_no_saved_customers(client):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []