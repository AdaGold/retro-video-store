from flask import current_app
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Table, Column, Integer, ForeignKey # OR line2?
from app import db
from app.models.customer import Customer


class Video(db.Model):
    __tablename__="videos"

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True, default=None) # default=None correct?
    total_inventory = db.Column(db.Integer, default=0)  
    


    def video_get_json(self):
        return {
            "id":self.video_id,
            "title":self.title,
            "release_date":self.release_date,
            "total_inventory":self.total_inventory,
            }