import pytest
from app import create_app
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
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
def one_rental(app):
    c = Customer(name = "minh",
                postal_code = 98123,
                phone = "555-555-5555",
                register_at = datetime.utcnow())

    v = Video(title = "Howls Moving Castle",
            release_date = "2005-07-17",
            total_inventory = 10)

    r = Rental(customer_id = 1,
                video_id = 1)
    
    db.session.add(c)
    db.session.add(v)
    db.session.commit()
    db.session.add(r)
    db.session.commit()



@pytest.fixture
def one_customer(app):
    c = Customer(name = "minh",
                postal_code = 98123,
                phone = "555-555-5555",
                register_at = datetime.utcnow())

    db.session.add(c)
    db.session.commit()


@pytest.fixture
def two_customers(app):
    c1 = Customer(name = "minh",
                postal_code = 98123,
                phone = "555-555-5555",
                register_at = datetime.utcnow())

    c2 = Customer(name = "summer",
                postal_code = 98123,
                phone = "444-444-4444",
                register_at = datetime.utcnow()) 
    
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()


@pytest.fixture
def one_video(app):
    v = Video(title = "Howls Moving Castle",
            release_date = "2005-07-17",
            total_inventory = 10)

    db.session.add(v) 
    db.session.commit()


@pytest.fixture
def two_videos(app):
    v1 = Video(title = "Howls Moving Castle",
            release_date = "2005-07-17",
            total_inventory = 10)
    
    v2 = Video(title = "10 Things I Hate About You",
            release_date = "1999-03-31",
            total_inventory = 3)

    db.session.add(v1)
    db.session.add(v2)
    db.session.commit()

# # This fixture gets called in every test that
# # references "one_task_belongs_to_one_goal"
# # This fixture creates a task and a goal
# # It associates the goal and task, so that the
# # goal has this task, and the task belongs to one goal
# @pytest.fixture
# def one_task_belongs_to_one_goal(app, one_goal, one_task):
#     task = Task.query.first()
#     goal = Goal.query.first()
#     goal.tasks.append(task)
#     db.session.commit()
