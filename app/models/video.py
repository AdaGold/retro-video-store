from flask import current_app
from flask.helpers import make_response
from app import db
from sqlalchemy import DateTime

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer,default=0, nullable = True)
    customers = db.relationship('Customer', back_populates='videos', secondary='rentals')
    # rentals = db.relationship('Rental', backref='rental', lazy=True)

    def to_json(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }