from flask import current_app
from app import db

class Rental(db.Model):
    __tablename__ = "rental"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id")) 
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.Date)

    def to_json_rental(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
        }