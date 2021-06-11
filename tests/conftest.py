import pytest
from app import create_app
from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental
from app import db
from datetime import datetime


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_customer(app):
    new_customer = Customer(
            name="Bob Ross", postal_code="12345", phone="123456", registered_at=datetime.now(), videos_checked_out_count=0)
    db.session.add(new_customer)
    db.session.commit()


@pytest.fixture
def three_customers(app):
    db.session.add_all([
        Customer(
            name="Bob Ross", postal_code="12345", phone="123456", registered_at=datetime.now(), videos_checked_out_count=0),
        Customer(
            name="Michelangelo", postal_code="54321", phone="654321", registered_at=datetime.now(), videos_checked_out_count=0),
        Customer(
            name="Alfred - Wayne Family Butler", postal_code="77777", phone="777777", registered_at=datetime.now(), videos_checked_out_count=0)
    ])
    db.session.commit()


@pytest.fixture
def one_video(app):
    new_video = Video(title="Batman Begins", release_date=datetime.now(), total_inventory=5, available_inventory=5)
    db.session.add(new_video)
    db.session.commit()


@pytest.fixture
def four_videos(app):
    db.session.add_all([
        Video(
            title="Batman Begins", release_date=datetime.now(), total_inventory=5, available_inventory=5),
        Video(
            title="The Dark Knight", release_date=datetime.now(), total_inventory=3, available_inventory=3),
        Video(
            title="The Dark Knight Rises", release_date=datetime.now(), total_inventory=7, available_inventory=7),
        Video(
            title="Cartoon Batman", release_date=datetime.now(), total_inventory=4, available_inventory=4)
    ])
    db.session.commit()


@pytest.fixture
def six_rentals(app, three_customers, four_videos):
    customers = Customer.query.all()
    i = 1
    for customer in customers:
        video = Video.query.get(i)
        video2 = Video.query.get(i+1)
        new_rental = Rental(customer_id=customer.id, 
                        video_id=video.id,
                        checkout_date=datetime(2021, (4-i), 13, 17, 30, 29),
                        due_date=datetime(2021, (4-i), 20, 17, 30, 29),
                        check_in_date=None)
        new_rental2 = Rental(customer_id=customer.id, 
                        video_id=video2.id,
                        checkout_date=datetime(2021, (6-i), 8, 17, 30, 29),
                        due_date=datetime(2021, (6-i), 15, 17, 30, 29),
                        check_in_date=datetime(2021, (6-i), 11, 17, 30, 29))
        customer.videos_checked_out_count += 2
        video.available_inventory -= 1
        video2.available_inventory -=1
        db.session.add(new_rental)
        db.session.add(new_rental2)
        db.session.commit()
        i += 1