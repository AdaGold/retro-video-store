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
    total_inventory = db.Column(db.Integer,default=0)
    available_inventory = db.Column(db.Integer,default=0)
    

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
    
    def decrease_inventory(self):
        """
            Input:  instance of Video
            Output: decreased availablity inventory for instance of Video
        """

        self.available_inventory = self.available_inventory - 1
        db.session.commit()
    
    
    def increase_inventory(self):
        """
            Input:  instance of Video
            Output: increase availablity inventory for instance of Video
        """
        
        self.available_inventory = self.available_inventory + 1
        db.session.commit()