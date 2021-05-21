from sqlalchemy.orm import relationship
from datetime import datetime
from app import db



class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    
    videos_checked_out = db.relationship('Rental', backref='customer', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'postal_code': self.postal_code,
            'registered_at': self.registered_at,
            'videos_checked_out_count': len(self.videos_checked_out)
        }
