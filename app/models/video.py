from app import db
from flask import current_app
from sqlalchemy import DateTime


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    # lowercase 'goal.id' looks at a table in your db
    # goal_id = db.Column(db.Integer, db.ForeignKey(
    #     'goal.goal_id'), nullable=True)

    def is_complete(self):
        if self.completed_at:
            return True
        else:
            return False

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

    def with_goal(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete(),
            "goal_id": self.goal_id
        }
