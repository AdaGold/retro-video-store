from flask import current_app
from app import db
# from flask_migrate import Migrate


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)    # 200 enough for names?
    register_at = db.Column(db.DateTime) 
    postal_code = db.Column(db.Integer) 
    phone = db.Column(db.Integer) 
    # videos_chekced_out_count =  db.Column(db.Integer, db.ForeignKey("video.video_id"), nullable=True)
    videos_checked_out_count =  db.Column(db.Integer)

    # need to fix
    def register_at(self):  #combine to get_json???
        is_register = self.register_at
        if is_register== None:
            register_at=False
        else:
            register_at = True
        return register_at

    def get_json(self):
        if self.video_id==None:
            return {
            "id":self.id,
            "name":self.name,
            "register_at":self.register_at,
            "postal_code":self.postal_code,
            "phone":self.phone,
            "videos_checked_out_count":self.videos_checked_out
            }
        else:
            return {
            "id":self.id,
            "name":self.name,
            "register_at":self.register_at,
            "postal_code":self.postal_code,
            "phone":self.phone,
            "videos_checked_out_count":self.videos_checked_out
            }
            