from flask import current_app, make_response
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_copies = db.Column(db.Integer)
    availible_inventory = db.Column(db.Integer)
    # customers = db.relationship("Rental", back_populates="customers")

    def make_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_copies,
            "availible_inventory": self.availible_inventory
                    }
                    
    def return_id(self):
        return {"id":self.id}
    
    def check_out(self):
        if self.availible_inventory == 0:
            return None

        else:
            # self.availible_inventory = self.availible_inventory -1
            self.availible_inventory -= 1
    
    def check_in(self):
        self.availible_inventory += 1
        # if self.availible_inventory is None:
        #     self.availible_inventory = 1
        # else:
        #     self.availible_inventory = self.availible_inventory +1
