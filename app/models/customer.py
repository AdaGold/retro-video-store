from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from flask import make_response, jsonify, abort


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer)


    def json_response(self): 
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone

        }

    


    
    