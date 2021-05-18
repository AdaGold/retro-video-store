from flask import current_app
from app import db 
from sqlalchemy.orm import relationship



class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64))
    customer_zip = db.Column(db.String(5))
    customer_phone = db.Column(db.String(14))
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)
    videos = relationship("Rental", back_populates="customer")
    


    def to_json(self):
        customer_dictionary = { "id": self.customer_id, 
                                "name": self.customer_name, 
                                "postal_code": self.customer_zip, 
                                "phone": self.customer_phone, 
                                "registered_at": self.register_at, 
                                "videos_checked_out_count": self.videos_checked_out_count,
                                }
        return customer_dictionary




    # @classmethod
    # def new_customer_from_json(cls, body):
    #     new_customer = Customer(customer_name=body["name"], customer_zip=body["postal_code"], customer_phone=body["phone"])
    #     return new_customer
