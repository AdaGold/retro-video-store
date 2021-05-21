from app import db

class Rental(db.Model):
    __tablename__ = "rentals"
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"), primary_key=True)