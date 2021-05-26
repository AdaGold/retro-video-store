from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable = False)
    videos_checked_out = db.Column(db.Integer, default=0)
    videos = db.relationship("Rental", back_populates="customer")
    
    def make_json(self):
        """
        Takes in an instance of Customer 
        returns id, name, registered_at, postal_code,
        phone and videos_checked_out_count of that Customer 
        instance in a JSON compatabile dictionary

        """
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": str(self.postal_code),
            "phone": self.phone_number,
            "videos_checked_out_count": self.videos_checked_out
        }
    def return_id(self):
        """
        Takes in an instance of Customer 
        returns the id of that Customer instance in a 
        JSON compatabile dictionary

        """
        return {"id":self.id}

    def check_out(self):
        """
        Takes in an instance of Customer 
        Increases the videos_checked_out by 1

        """
        self.videos_checked_out += 1

    def check_in(self):
        """
        Takes in an instance of Customer 
        Decreases the videos_checked_out by 1

        """
        self.videos_checked_out -= 1
        