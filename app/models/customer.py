
from flask import current_app
from app import db
from datetime import date, timedelta




class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def build_dict(self):
        customer_dict = {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "registered_at" : self.registered_at,
            "videos_checked_out_count" : self.videos_checked_out_count
        } 
        return customer_dict
    
    # def rent_video(self, video):
    #     return {
    #         "customer_id" :  self.id,
    #         "video_id" : video.id,
    #         "due_date" : date.today() + timedelta(7),
    #         # "videos_checked_out_count" : len(self.get_videos()),
    #         "available_inventory" : (video.available_inventory) - 1
    #     }
    # def return_video(self, video):
    #     return {
    #         "customer_id" :  self.id,
    #         "video_id" : video.id,
    #         # "videos_checked_out_count" : len(self.get_videos()),
    #         "available_inventory" : video.available_inventory
    #     }
    
