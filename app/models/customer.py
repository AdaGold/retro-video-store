from app import db

# make a new class inheriting from db.Model (the SQLAlchemy object - SQL like singular class names):
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)

    
    ### this is to change the name of the table, so it doesn't use the default class name:
    __tablename__="customers"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "registered_at": self.registered_at
        }

