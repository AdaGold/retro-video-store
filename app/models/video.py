from sqlalchemy.orm import backref,relationship
from app import db
#from app.models.customer import Customer


class Video(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String)
    release_date=db.Column(db.String)
    total_inventory=db.Column(db.Integer) #required
   
    #decrease by one with rentals/checkout
    available_inventory=db.Column(db.Integer,default=0)
    customers=relationship("Customer", secondary="rental")
    
    def available_inventory(self):
        #decreases available inventory by one for check-out
        return self.total_inventory-len(self.customers)

    def check_in_inventory(self):
        #increases available inventory by one for check
        return self.total_inventory+len(self.customers)

    def video_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory()
        }