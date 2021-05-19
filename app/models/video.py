from app import db
from dataclasses import dataclass
import datetime

@dataclass
class Video(db.Model): 
    id: int
    title: str
    release_date: datetime
    total_inventory: int
    available_inventory: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime) # nullable = True
    total_inventory = db.Column(db.Integer, default=0, nullable = True)
    available_inventory = db.Column(db.Integer, default=0, nullable = True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)

    def to_dictionary(self):
        '''
        Outputs a dictionary format of the video object
        '''
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            } 

        # if self.customer_id:
        #     return {
        #         "id": self.id,
        #         "title": self.title,
        #         "release_date": self.release_date,
        #         "total_inventory": self.total_inventory,
        #         "available_inventory": self.available_inventory,
        #         "customer_id": self.customer_id
        #         } 
        # else: 
        #     return {
        #         "id": self.id,
        #         "title": self.title,
        #         "release_date": self.release_date,
        #         "total_inventory": self.total_inventory,
        #         "available_inventory": self.available_inventory
        #         } 