from sqlalchemy.orm import relationship
from app import db
import datetime


class Rental(db.Model):
    customer_id = db.Column("customer_id", db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column("video_id", db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    video = relationship("Video", back_populates="customers")
    customer = relationship("Customer", back_populates="videos")
    due_date = db.Column(db.Date(), default=datetime.date.today() + datetime.timedelta(days=7))

    def as_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": Customer.query.get(self.customer_id).get_checked_count(),
            "available_inventory": Video.query.get(self.video_id).get_inventory()
        }


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime())
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos = relationship("Rental", back_populates="customer")

    def as_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.get_checked_count()}

    def get_checked_count(self):
        return len(self.videos)

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date())
    total_inventory = db.Column(db.Integer)
    customers = relationship("Rental", back_populates="video")

    def as_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.get_inventory()}

    def get_inventory(self):
        return self.total_inventory - len(self.customers)