from flask import current_app
from app import db
from .rental import Rental
from datetime import datetime

class Customer(db.Model):
    """
    Attributes:
        name 
        postal code
        phone 
        registered_at
        videos_checked_out_count
    """
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.String,nullable=False)
    registered_at = db.Column(db.DateTime,default=datetime.utcnow())#registers when customer is entered into the sytstem
    videos_checked_out_count = db.Column(db.Integer,default=0)
    rentals = db.relationship("Rental", backref='customer',lazy=True)#creates ghost column with a list of video_ids each customer has checked out gathered through the Rental table 
  
    
    def to_python_dict(self):
        """
            Input: instance of Customer
            Output: returns a python dictionary of Customer instance

        """
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count,
            "registered_at": self.registered_at
            }

    def increase_checkout_count(self):
        """
            Input:  instance of cutomer
            Output: increases videos_checked_out_count attribute in customer by 1
        """
        self.videos_checked_out_count = self.videos_checked_out_count + 1
        db.session.commit()
    
    def decrease_checkout_count(self):
        """
            Input:  instance of cutomer
            Output: decreases videos_checked_out_count attribute in customer by 1
        """
        self.videos_checked_out_count = self.videos_checked_out_count - 1
        db.session.commit()