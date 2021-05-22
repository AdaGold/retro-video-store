from sqlalchemy.orm import relationship
from datetime import datetime
from app import db



class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_inventory = db.Column(db.Integer)

    rentals = db.relationship('Rental', backref='video', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'total_inventory': self.total_inventory
        }

    @property
    def available_inventory(self):
        return self.total_inventory - len(self.rentals)




