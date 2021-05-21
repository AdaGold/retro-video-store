
from flask import current_app
from app import db
from datetime import date, timedelta




class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out = db.relationship('Rental', backref= 'rentals', lazy=True)

    def count_videos(self):
        #counts videos in videos_checked_out
        return len([vid for vid in self.videos_checked_out])

    def build_dict(self):
        #builds customer dictionary
        customer_dict = {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "registered_at" : self.registered_at,
            "videos_checked_out_count" : self.count_videos()
        } 
        return customer_dict
    

