from flask import current_app
from app import db
# from app.models.video import Video
# from app.models.customer import Customer

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id"))
    due_date = db.Column(db.DateTime)
