from flask import current_app
from app import db
from datetime import datetime

# association table for many to many relationship between customer and video
association_table = db.Table('customer_videos',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.video_id'))
)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String) 
    register_at = db.Column(db.DateTime, nullable=False)
    #establish relationship
    videos_checked_out = db.relationship('Video', secondary=association_table, backref=db.backref('customers', lazy=True))

    def details_of_customer_response(self):
        return {
                "id": self.customer_id,
                "name": self.name,
                "registered_at": self.register_at,
                "postal_code": self.postal_code,
                "phone": self.phone_number,
                "videos_checked_out_count": len(self.videos_checked_out)
                }

    def add_new_customer(self):
        return{
            
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number
        }
      
      
class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
  
    customer_vids = db.relationship('customer_vids', secondary=association_table, backref=db.backref('videos', lazy=True))
    
    def calculate_available_inventory(self):
        pass
    
    def video_response(self):
        return  {
                    "id": self.video_id,
                    "title": self.title,
                    "release_date": self.release_date,
                    "total_inventory": self.total_inventory,
                    "available_inventory": self.calculate_available_inventory()
                }