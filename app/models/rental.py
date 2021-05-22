from app.models.video import Video
from app.models.customer import Customer
from flask import current_app
from app import db
from datetime import timedelta, datetime
from sqlalchemy.orm import relationship, backref

# association table 
class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id')) #foreign coming from customer model 
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id')) #foreign coming from video model 
    due_date = db.Column(db.DateTime, nullable = True, default = datetime.now() + timedelta(days=7)) 
    # create a due date. The rental's due date is the seven days from the current date
    customer = relationship("Customer", backref="rentals", lazy=True)
    video = relationship("Video", backref="rentals", lazy=True)

    def to_json_rental(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date":self.due_date,
            "videos_checkout_out":self.customer.videos_checked_out_count,
            "available_inventory":self.video.available_inventory
        }


