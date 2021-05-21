from flask import current_app
from app import db
# from app.models.video import Video
# from app.models.rental import Rental
# from flask_sqlalchemy import SQLAlchemy


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, nullable = True)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    # videos = db.relationship("Video", secondary="rental", lazy=True)


    def json_response(self):
        response = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
            }

        return response