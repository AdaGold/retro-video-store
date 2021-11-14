from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
   

#helper function to return dict
    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "registered_at" : datetime.now()
        }