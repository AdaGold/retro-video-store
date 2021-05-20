from app import db
from datetime import datetime
from flask import current_app
from sqlalchemy.orm import backref,relationship
#from app.models.rental import Rental

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    postal_code=db.Column(db.String)
    phone=db.Column(db.String) 
    registered_at=db.Column(db.DateTime, nullable=True, default=None)
    
    #join_clause=db.relationship("Video",secondary=Rental, backref=db.backref('subscribers'), lazy='dynamic')
    #should increase by one, when rental checked out
    #videos_checked_out_count=db.Column(db.Integer) 
    videos=relationship("Video", secondary = "rental")
    #videos_checked_out_count=db.Column(db.Integer,default=0)
    # def video_count(self):
    #     if self.id == None:
    #         pass
    #     else:
    #         return 0

    def videos_checked_out_count(self):
        #increases customer's video checked out count for check out
        return len(self.videos)

    def check_in_video_count(self):
        return len(self.videos)+1

    def customer_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count()
        }