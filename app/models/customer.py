from flask import current_app
from app import db
from .video import Video

class CustomerVideoJoin(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos_checked_out = db.Column(db.Integer, nullable=True)
    
    def get_videos(self):
        join_results = db.session.query(Customer, Video, CustomerVideoJoin).join(Customer, Customer.id==CustomerVideoJoin.customer_id).join (Video, Video.id==CustomerVideoJoin.video_id).filter(Customer.id == self.id).all()
        return len(join_results)

    def build_dict(self):
        customer_dict = {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "register_at" : self.register_at,
            "videos_checked_out" : self.get_videos()
        } 
        return customer_dict
    
