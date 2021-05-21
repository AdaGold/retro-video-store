from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    title = db.Column(db.String) 
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False) 
    # Video has many Rentals, and a Rental belongs to a Video
    rentals = db.relationship("Rental", backref="video")

    def video_to_json_response(self):
        '''
        Converts a Video instance into JSON format
        Output: Returns a Python dictionary in the shape of JSON response 
        that the API returns in the route that is called (GET route).
        '''
        #  Release date format:  "1979-01-18",("%Y-%m-%d")
        return  {"id": self.id,
                "title": self.title,
                "release_date": self.release_date.strftime("%Y-%m-%d"), 
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory}
                
    @staticmethod
    def from_json_to_video(request_body):
        '''
        Converts JSON request body into a new instance of Customer
        input: Takes in a dictionary in the shape of the JSON the API 
        receives. 
        '''
        new_video = Video(title=request_body["title"],
                release_date=request_body["release_date"],
                available_inventory = request_body["total_inventory"],
                total_inventory = request_body["total_inventory"])

        return new_video

