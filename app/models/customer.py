from flask import current_app
from app import db
from .rental import Rental

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
    name = db.Column(db.String,nullable=False)#required attributes
    postal_code = db.Column(db.String,nullable=False)#required attributes
    phone = db.Column(db.String,nullable=False)#required attributes
    registered_at = db.Column(db.DateTime,nullable=True)
    videos_checked_out_count = db.Column(db.Integer,default=0)
    
  
    
    def to_python_dict(self):
        """
            Input: instance of Customer
            Output: returns a python dictionary of Customer instance

        """
        return {
            
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
            }
