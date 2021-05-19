from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos_rent = db.relationship('Video', secondary='rental', backref=db.backref('renters',lazy='dynamic'))
    
    def to_json(self):
        customer = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.register_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer
      
    @classmethod  
    def from_json(cls, json_file):
        return cls(**json_file)