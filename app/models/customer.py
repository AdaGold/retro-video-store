from app import db
from flask import current_app
from sqlalchemy import DateTime


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, default=0)

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

    # def with_goal(self):
    #     return {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": self.is_complete(),
    #         "goal_id": self.goal_id
    #     }
