
from flask import Flask, current_app
from app import db
from flask_sqlalchemy import SQLAlchemy


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def resp_json(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.total_inventory
        }