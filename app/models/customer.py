from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String, nullable = False)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    movies_checked_out = db.Column(db.Integer, default = 0)


    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": datetime.utcnow(),
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.movies_checked_out
        }
