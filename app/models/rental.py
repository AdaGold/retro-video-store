from flask import current_app
from app import db
from dataclasses import dataclass 



@dataclass
class Rental(db.Model):
    id: int 
    customer_id: int 
    video_id: int 
    due_date: str 
    
    

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.String)


   