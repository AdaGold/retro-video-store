# from flask import current_app
from app import db

class Rental(db.Model):
    __tablename__ = "videos_customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    due_date = db.Column(db.DateTime)

    def to_dict(self, checked_out, available_inventory):
        return {
                "video_id": self.video_id,
                "customer_id": self.customer_id,
                "videos_checked_out_count": checked_out,
                "available_inventory": available_inventory
                }