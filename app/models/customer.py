from app import db

# make a new class inheriting from db.Model (the SQLAlchemy object - SQL like singular class names):
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    # One to many relationship: one customer has many rentals
    customers = db.relationship("Rental", backref="customers", lazy=True)  

    __tablename__= "customers"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }

