from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime, timedelta



class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, default=datetime.utcnow()+timedelta(days=7))
