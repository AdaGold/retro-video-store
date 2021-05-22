from app import db

class Rental(db.Model):
    __tablename__ = "rentals"
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))
    customers = db.relationship("Customer", backref="rentals")
    videos = db.relationship("Video", backref="rentals")

    