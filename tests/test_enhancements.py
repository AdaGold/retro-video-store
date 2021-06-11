from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental

#This test isn't testing an optional enhancement, it's just a practice test to make sure everything is working
def test_check_out_rental(client, one_customer, one_video):
    # Act
    response = client.post("/rentals/check-out", json={"customer_id": 1, "video_id": 1})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "customer_id" in response_body
    assert "due_date" in response_body
    assert "video_id" in response_body
    assert len(Customer.query.get(1).videos) == 1


def test_get_overdue_rentals_three_rentals(client, six_rentals):
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [{
            "video_id": 1,
            "title": "Batman Begins",
            "customer_id": 1,
            "name": "Bob Ross",
            "postal_code": "12345",
            "checkout_date": "Sat, 13 Mar 2021 17:30:29 GMT",
            "due_date": "Sat, 20 Mar 2021 17:30:29 GMT"
            },{
            "video_id": 2,
            "title": "The Dark Knight",
            "customer_id": 2,
            "name": "Michelangelo",
            "postal_code": "54321",
            "checkout_date": "Sat, 13 Feb 2021 17:30:29 GMT",
            "due_date": "Sat, 20 Feb 2021 17:30:29 GMT"
            }, {
            "video_id": 3,
            "title": "The Dark Knight Rises",
            "customer_id": 3,
            "name": "Alfred - Wayne Family Butler",
            "postal_code": "77777",
            "checkout_date": "Wed, 13 Jan 2021 17:30:29 GMT",
            "due_date": "Wed, 20 Jan 2021 17:30:29 GMT"
            }]


def test_get_video_history(client, six_rentals):
    # Act
    response = client.get("videos/3/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
            "customer_id": 2,
            "name": "Michelangelo",
            "postal_code": "54321",
            "checkout_date": "Thu, 08 Apr 2021 17:30:29 GMT",
            "due_date": "Thu, 15 Apr 2021 17:30:29 GMT"
            }]


def test_get_customer_history(client, six_rentals):
    # Act
    response = client.get("customers/2/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
                "title": "The Dark Knight Rises",
                "checkout_date": "Thu, 08 Apr 2021 17:30:29 GMT",
                "due_date": "Thu, 15 Apr 2021 17:30:29 GMT"
    }]