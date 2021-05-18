from flask import current_app
from app import db
from sqlalchemy import DateTime
from app.models.customer_video_join import association_table


class Customer(db.Model):
    __tablename__ = 'left'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out = db.Column(db.Integer, nullable=True, default=0)
    videos = db.relationship(
        "Video",
        secondary=association_table,
        back_populates="customers")

    def to_json(self):
        customer = {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": self.phone,
            "videos_checked_out_count": self.videos_checked_out
        }