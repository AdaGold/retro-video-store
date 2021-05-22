from flask import current_app
from app import db
from sqlalchemy.orm import relationship
# from datetime import datetime
# from sqlalchemy import Table, Column, Integer, ForeignKey # Need?

class Rental(db.Model):
    __tablename__ = "rental"

    rental_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    # video_id = db.Column(db.Integer, db.ForeignKey('customer.customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'),nullable=True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=True)

    due_date = db.Column(db.DateTime, nullable=True)
    # due_date = db.Column(db.DateTime, nullable=True, default=((datetime.today)+(datetime.timedelta(days=7))))
    # customer = relationship("Customer", back_populates="video")
    # video = relationship("Video", back_populates="customer")

    def rental_get_json(self):
        return {
            "id":self.rental_id,
            "name":self.name,
            "registered_at":self.register_at,
            "postal_code":int(self.postal_code),
            "phone":self.phone,
            "videos_checked_out_count":self.videos_checked_out_count
            }