from app import db
import datetime
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey


# this is telling flask about my database task table

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=1)
    
    #turning my dictionary into a json object
    
    def json_object(self):
        
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
    