from flask import current_app
from app import db
from sqlalchemy import func


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    # server_default is best practice and sets datetime at server. 
    # better practice to use func.now() which calculates time at server
    # more --> https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    # could spend more time on zones/formatting but hear students talking about confliting tests
    registered_at = db.Column(db.DateTime, server_default=func.now())
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos = db.relationship("Rental", back_populates="customer")


    def get_customer_data_structure(self):
        customer_data_structure = {
                    "id":self.id,
                    "name":self.name,
                    "registered_at":self.registered_at,
                    "postal_code": self.postal_code,
                    "phone": self.phone,
                    "videos_checked_out_count": self.videos_checked_out_count
                }

        return customer_data_structure
