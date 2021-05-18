from flask import current_app
from app import db

class Video(db.Model):
    """ 
        Attributes:
            title
            release_date
            total_inventory
            available_inventory
    """
    id =  db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable=False)
    release_date = db.Column(db.DateTime,nullable=False)
    total_inventory = db.Column(db.Integer,nullable=False)
    available_inventory = db.Column(db.Integer,nullable=True)
    #backref invisible attribute 'customer'. I can use video.customer to access this attribue value 

    def to_python_dict(self):
        """
            Input : instance of Video
            Output: python dict of Video instance
        """
        
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }