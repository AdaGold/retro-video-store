from flask import current_app, make_response
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_copies = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer, default=0)
    customers = db.relationship("Rental", back_populates="video")
    # customers = db.relationship("Rental", backref="video", lazy=True)
    

    def make_json(self):
        """
        Takes in an instance of Video 
        returns id, title, release_date, 
        total_inventory and first calulates and then 
        returns available_inventory of that Video 
        instance in a JSON compatabile dictionary

        """
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_copies,
            "available_inventory": self.get_available_inventory()
                    }
                    
    def return_id(self):
        """
        Takes in an instance of Video 
        returns the id of that Video instance in a 
        JSON compatabile dictionary

        """
        return {"id":self.id}

    def get_available_inventory(self):
        """
        Takes in an instance of Video 
        returns the number of total copies of that 
        Video minus the number of copies currently 
        checked-out by customers

        """
        return self.total_copies - len(self.customers)

