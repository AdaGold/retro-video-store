from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship, back_populate
# from app.models.video import Video

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=True, default=None)
    videos_checked_out_count = db.Column(db.Integer, default=0, nullable=False)
    videos = db.relationship("Rental", back_populates="customer")

#all other options i saw???
    # rentals = db.relationship('Rental', backref='customers', lazy=True)
        
    # videos = db.relationship("Video", secondary="rentals")
    # rentals = db.relationship("Video", secondary="rentals", lazy='subquery',backref=db.backref('customers', lazy=True))
    
    #do i need the db. before relationships? what i saw online didnt have it
    # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True) 

    # maybe create a method to see if video.video_checked_out_count:
    #     else" set to 1. 


    def api_response(self): 
        response_body = {
                        "id": self.id,
                        "name": self.name,
                        "registered_at": self.created,
                        "postal_code": self.postal_code,
                        "phone": self.phone,
                        "videos_checked_out_count": 0
                        }

        return response_body
