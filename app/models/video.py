from app import db
from flask import current_app
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, backref


class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    rentals = db.relationship('Rental', backref='rental', lazy=True)

    # customers = db.relationship(
    #     'Customer', secondary='rentals', back_populates='videos')

    # lowercase 'goal.id' looks at a table in your db

    def to_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory}
