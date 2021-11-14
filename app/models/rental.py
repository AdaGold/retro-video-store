from app import db
import datetime

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime, default = datetime.datetime.now() + datetime.timedelta(days=7)) 
    