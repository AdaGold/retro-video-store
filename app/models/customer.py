from app import db

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), nullable=True)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def to_dict(self): 
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
            }
