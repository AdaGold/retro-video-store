from flask import current_app
from app import db
from app.models.video import Video

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=True, default=None)

    # __tablename__ = "Customer"
    # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True) 

    def api_response(self): 
        response_body = {
                        "id": self.id,
                        "name": self.name,
                        #below needs to change
                        "registered_at": self.created,
                        "postal_code": self.postal_code,
                        "phone": self.phone,
                        #below needs to change
                        "videos_checked_out_count": 0
                        }

        return response_body
