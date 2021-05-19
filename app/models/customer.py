from flask import current_app #func to access data about the running application, including the configuration
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    #wave2 establish relationship
    #videos_checked_out_count = db.relationship("Video", secondary="Rental", backref="customers", lazy=True)

    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.register_at,
            "videos_checked_out_count": 0
        }