from flask import current_app
from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.Datetime)
    #videos_checked_out = 

    def to_json(self):
        id = self.id
        name = self.name
        postal_code = self.postal_code 
        phone = self.phone
        registered_at = self.registered_at

