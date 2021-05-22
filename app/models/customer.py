from app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String, nullable = False)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), default = datetime.now(timezone.utc))
    videos_checked_out_count = db.Column(db.Integer, default = 0)
    videos = relationship("Rental", back_populates="customer")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
