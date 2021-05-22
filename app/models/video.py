from flask import current_app, make_response
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_copies = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer, default=0)
    customers = db.relationship("Rental", back_populates="video")
    # customers = db.relationship("Rental", backref="video", lazy=True)
    

    def make_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_copies,
            "available_inventory": self.get_available_inventory()
                    }
                    
    def return_id(self):
        return {"id":self.id}

    def get_available_inventory(self):
        return self.total_copies - len(self.customers)

