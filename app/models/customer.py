from app import db
import datetime
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable = True)
    rentals = db.relationship('Rental', backref = 'customer', lazy=True)
    #videos = db.relationship("Video", secondary="rental", back_populates="customers")

#helper function to return dict
    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "registered_at" : datetime.now()
        }

    def videos_rental_query_by_customer(self):
        rental_query = Rental.query.filter_by(customer_id = self.id)
        return rental_query.count()