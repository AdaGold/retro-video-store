from app import db
from flask import current_app
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, backref


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    # videos = db.relationship(
    #     'Video', secondary='rentals', back_populates='customers')

    rentals = db.relationship('Rental', backref='rentals', lazy=True)

    # lowercase 'goal.id' looks at a table in your db
    # goal_id = db.Column(db.Integer, db.ForeignKey(
    #     'goal.goal_id'), nullable=True)

    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": int(self.postal_code),
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count}
