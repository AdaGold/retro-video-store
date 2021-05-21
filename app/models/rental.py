from flask import current_app
from app import db
from app.models.customer import Customer
from app.models.video import Video

class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime)
    # Why do we need these tw`o lines below if we have the video/customer keys? 
    customer = db.relationship('Customer', backref='customer_with_video',lazy=True)
    video = db.relationship('Video', backref='rented_video', lazy=True)

    def get_rental_response(self):
        return {
            "customer_id":self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": len(Customer.query.get(self.customer_id).rentals),
            "available_inventory": (Video.query.get(self.video_id).total_inventory - len(Video.query.get(self.video_id).active_rentals))}