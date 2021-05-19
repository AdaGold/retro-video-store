from app import db
import datetime
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory= db.Column(db.Integer)
    

 # helper function  display  json
    def display_json(self):
        return {
                "id": self.video_id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": 10,
                "available_inventory": 0
                }  