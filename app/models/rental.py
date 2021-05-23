from app import db
from sqlalchemy.orm import relationship

class Rental(db.Model):
    __tablename__ = "rental"
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column("customer", db.Integer, db.ForeignKey("customer.customer_id"), primary_key=True)
    video_id = db.Column("video", db.Integer, db.ForeignKey("video.video_id"), primary_key=True)
    due_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
            }