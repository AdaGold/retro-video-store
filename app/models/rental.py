from app import db

# make a new class inheriting from db.Model (the SQLAlchemy object - SQL like singular class names):
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.relationship("Customer", backref="rentals", lazy=True)   # This helps us find a rental's related customers with rental.customers and a customer's related rental with customer.rentals (as in the "rentals" table, not "many rentals")
    video_id = db.relationship("Video", backref="rentals", lazy=True)   # This helps us find a rental's related videos with rental.videos and a video's related rental with video.rentals (as in the "rentals" table, not "many rentals")

    __tablename__= "videos"

    def to_dict(self):

        return {
            "id": self.id,
            "due_date": self.due_date
        }