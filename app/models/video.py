from flask import current_app
from sqlalchemy.orm import relationship
from app import db


# ❗️ Revisit this syntax and what it actually translates to
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# ❗️ Revisit this syntax and what it actually translates to
class Link(Base): 
    __tablename__ = 'link'
    match_video_id = db.Column(
        db.Integer, 
        db.ForeignKey('video.video_id'),
        primary_key=True
        ),

    match_cust_id = db.Column(
        db.Integer, 
        db.ForeignKey('customer.customer_id'),
        primary_key=True
        )



class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    # ideally this would be a list of customer ids:
    customers_of_video = db.relationship('Customer', 
                            secondary='link' 
                            )

    def convert_to_json(self):

        response_body = {  
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            # 
            # "available_inventory": 
        }


        return response_body