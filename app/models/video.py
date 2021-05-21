from flask import current_app
from app import db 

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

def video_to_json(self):
    return {
        "id" : self.id,
        "title" : self.title,
        "release_date" : self.release_date,
        "total_inventory" : self.total_inventory
        #"active_rentals" : (self.total_inventory - len(self.active_rentals)
    }
