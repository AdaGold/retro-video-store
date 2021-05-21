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
def three_videos(app):
    db.session.add_all([
        Video(
            title="Batman Begins", release_date=datetime.now(), total_inventory=5, available_inventory=5),
        Video(
            title="The Dark Knight", release_date=datetime.now(), total_inventory=3, available_inventory=3),
        Video(
            title="The Dark Knight Rises", release_date=datetime.now(), total_inventory=7, available_inventory=7)
    ])
    db.session.commit()

@pytest.fixture
def one_rental(app, one_customer, one_video):
    customer = Customer.query.first()
    video = Video.query.first()
    new_rental = Rental(customer_id=customer.id, video_id=video.id, due_date=datetime(2021, 4, 23, 17, 30, 29))
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    db.session.add(new_rental)
    db.session.commit()

@pytest.fixture
def three_rentals(app, three_customers, three_videos):
    for i in range(1, 4):
        customer = Customer.query.get(i)
        video = Video.query.get(i)
        new_rental = Rental(customer_id=customer.id, video_id=video.id, due_date=datetime(2021, (7-i), 20, 17, 30, 29))
        customer.videos_checked_out_count += 1
        video.available_inventory -= 1
        db.session.add(new_rental)
        db.session.commit()