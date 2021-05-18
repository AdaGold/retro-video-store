from flask import current_app
from app import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_copies = db.Column(db.Integer)

def to_json(self):
    return {
        "id": self.id,
        "title": self.title,
        "release date": self.release_date,
        "total copies": self.total_copies
    }

