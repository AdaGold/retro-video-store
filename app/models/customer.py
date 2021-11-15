from app import db
from datetime import date
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=date.today())
    #rentals = db.relationship('Rental', backref = 'customer', lazy=True)
    videos = db.relationship("Video", secondary="rental", backref="customers")

#helper function to return dict
    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "registered_at" : self.registered_at
        }

    def videos_rental_query_by_customer(self):
        rental_query = Rental.query.filter_by(customer_id = self.id)
        return rental_query.count()