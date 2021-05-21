from app import db
from datetime import datetime
from app.models.rental import Rental

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    #rentals = db.relationship('Rental', backref= 'rentals', lazy=True)

    @classmethod
    def create(cls, name, postal_code, phone):
        new_customer = Customer(name=name, postal_code=postal_code, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @classmethod
    def read_all(cls):
        customers = Customer.query.all()
        return customers
        
    @classmethod
    def read(cls, customer_id):
        customer = Customer.query.get(customer_id)
        return customer

    @classmethod
    def update(cls, customer_id, name=None, postal_code=None, phone=None):
        customer = Customer.read(customer_id)
        if name:
            customer.name = name
        if postal_code:
            customer.postal_code = postal_code
        if phone:
            customer.phone = phone
        db.session.commit()
        return customer

    @classmethod
    def delete(cls, customer_id):
        customer = Customer.read(customer_id)
        db.session.delete(customer)
        db.session.commit()

    def to_dict(self):
        format_string = '%a, %-d %b %Y %H:%M:%S %z' # Wed, 16 Apr 2014 21:40:20 -0700
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at.strftime(format_string),
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        


        