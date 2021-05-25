from app import db
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at= db.Column(db.DateTime, default= datetime.now())
    videos_checked_out_count = db.Column(db.Integer, default=0, nullable=True)
    
    def cust_dict(self):
        return { 
                "id": self.customer_id,
                "name" : self.name,
                "postal_code" : self.postal_code,
                "phone" : self.phone, 
                "registered_at":self.registered_at,
                "videos_checked_out_count":self.videos_checked_out_count
                }

