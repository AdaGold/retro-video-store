from app.models.customer import Customer


def test_TEST(client):
    # Act
    response = client.post("/customers", json={
        "name": "Lars Sankar",
        "postal_code": "75007",
        "phone": "111-111-1111"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201

