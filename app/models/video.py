from flask import current_app
from app import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime(), nullable=True)
    total_inventory = db.Column(db.Integer, default=0)
    # available_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            # "available_inventory": self.available_inventory
        }

    # a foreign key column refers to the primary key of the other table
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True, default=None)

    # def to_dict(self):
    #     if self.goal_id:
    #         return {
    #             "id": self.id,
    #             "goal_id": self.goal_id,
    #             "title": self.title,
    #             "description": self.description,
    #             "is_complete": True if self.completed_at else False
    #     }
    #     else:
    #         return {
    #             "id": self.id,
    #             "title": self.title,
    #             "description": self.description,
    #             "is_complete": True if self.completed_at else False
    #     }

      