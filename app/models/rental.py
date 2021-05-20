from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import db



class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)



    def return_data(self):
        return_info = {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,

            }
        return return_info


# for customer, video in results: 
#     print(customer.name, video.name)


