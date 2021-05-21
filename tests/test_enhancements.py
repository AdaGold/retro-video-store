from datetime import datetime
from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental

#This test isn't testing an enhancement, it's just making sure all the testing stuff works
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


def test_get_overdue_rentals_one_rental(client, one_rental):
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
            "customer_id": 1,
            "video_id": 1,
            "due_date": "Fri, 23 Apr 2021 17:30:29 GMT",
            "videos_checked_out_count": 1,
            "available_inventory": 4
            }]


#In one month from now, this test won't pass (now = 21 May 2021)
def test_get_overdue_rentals_three_rentals(client, six_rentals):
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    #In one month from now len(response_body) == 6
    assert len(response_body) == 3
    assert response_body == [{
            "customer_id": 2,
            "video_id": 2,
            "due_date": "Thu, 20 May 2021 17:30:29 GMT",
            "videos_checked_out_count": 2,
            "available_inventory": 1
            },{
            "customer_id": 3,
            "video_id": 3,
            "due_date": "Tue, 20 Apr 2021 17:30:29 GMT",
            "videos_checked_out_count": 2,
            "available_inventory": 5
            }, {
            "customer_id": 3,
            "video_id": 4,
            "due_date": "Sat, 15 May 2021 17:30:29 GMT",
            "videos_checked_out_count": 2,
            "available_inventory": 3
            }]


def test_get_video_history(client, six_rentals):
    # Act
    response = client.get("videos/3/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
                "customer_id": 3,
                "name": "Alfred - Wayne Family Butler",
                "postal_code": "77777",
                "checkout_date": "Tue, 13 Apr 2021 17:30:29 GMT",
                "due_date": "Tue, 20 Apr 2021 17:30:29 GMT"
    }]

# def test_get_customer_history(client, six_rentals):
#     pass