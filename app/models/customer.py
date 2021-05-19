from flask import current_app
from app import db
# from sqlalchemy.orm import relationship
# from .task import Task

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    # if customer.registered_at == None:
    #         customer.registered_at = datetime.datetime.now()

    def to_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
