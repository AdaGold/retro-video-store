from app import db
from datetime import timedelta, datetime 


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column('video_id', db.Integer, db.ForeignKey('video.video_id'))
    check_out_date = db.Column('check_out_date', db.DateTime, default=datetime.now())
    renter = db.relationship('Customer', backref='rentals', lazy=True, foreign_keys=customer_id)
    video = db.relationship('Video', backref='rentals', lazy=True, foreign_keys=video_id)

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.check_out_date + (timedelta(days=7)),
            "videos_checked_out_count": self.renter.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }
