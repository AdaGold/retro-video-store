from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True) # autoincrement=True
    customer_name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_date = db.Column(db.DateTime, nullable = True)
    videos_checked_out_count = db.Column(db.Integer, default=0) #nullable false?

    #videos_checked_out_count = relationship("Rental", backref="rentals", lazy=True)

    def registered_at(self):
        #need to return a date/time here
        if self.register_date:
            return True
        else:
            return False

    def return_customer_info(self):
        return {"id" : self.customer_id,
        "name" : self.customer_name,
        "registered_at": self.registered_at(),
        "postal_code" : str(self.postal_code),
        "phone": self.phone_number, 
        "videos_checked_out_count": self.videos_checked_out_count       
        }
    
    # def added_checkout(self):
    #     #if self.videos_checked_out_count:
    #     self.videos_checked_out_count += 1
    #     # else:
    #     #     self.videos_checked_out_count = 0
    #     db.session.commit()



