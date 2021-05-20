from flask import current_app
from app import db
from datetime import date, timedelta
from .customer import Customer
from .video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.Date(), default = date.today() + timedelta(7), nullable=True)

    def build_dict(self):
        video = Video.query.get(self.video_id)
        customer = Customer.query.get(self.customer_id)

        rental = {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count" : customer.count_videos(),
            "available_inventory" : video.available_inventory
            }
        if self.due_date:
            rental["due_date"] = self.due_date
        return rental