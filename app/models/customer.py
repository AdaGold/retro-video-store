from flask import current_app
from app import db 

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    regristered_at = db.Column(db.DateTime)
    #rental_counts = db.relationship('Videos', backref='customer')

def customer_to_json(self):
    return {
        "id" : self.id,
        "name" : self.name,
        "registered_at" : self.register_at,
        "postal_code" : self.postal_code,
        "phone" : self.phone,
        "videos_checked_out_count" : 0}
