from app import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return{
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'due_date': self.due_date
        }