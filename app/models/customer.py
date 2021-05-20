from app import db
from flask import current_app
from sqlalchemy import DateTime


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, default=0, nullable=True)

    videos = db.relationship(
        'Video', secondary='rentals', back_populates='customers')

    # lowercase 'goal.id' looks at a table in your db
    # goal_id = db.Column(db.Integer, db.ForeignKey(
    #     'goal.goal_id'), nullable=True)

    # def is_complete(self):
    #     if self.completed_at:
    #         return True
    #     else:
    #         return False

    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count}
