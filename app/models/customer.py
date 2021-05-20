from sqlalchemy.orm import relationship
from app import db
from datetime import datetime, timezone


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos = relationship("Rental", back_populates="customer", cascade="all, delete")

    def as_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.get_checked_count()}

    def get_checked_count(self):
        return len(self.videos)
