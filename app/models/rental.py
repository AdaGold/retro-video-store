from app import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rentals'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return{

            
        }