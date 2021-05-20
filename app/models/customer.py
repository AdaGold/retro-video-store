from flask import current_app # faded font color suggests unnecessary
from app import db
from datetime import datetime # ^^ ??

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # adding of own volition, also found in postman tests
    name = db.Column(db.String(200))
    postal_code = db.Column(db.Integer) # 5 digit US postal code...account for other countries? that 4-digit ext for US codes?
    phone_number = db.Column(db.String(12)) # 10 digits and 2 '-' separators for formatting
    register_at = db.Column(db.DateTime) # no nullable bc doesnt make sense to for them to be in the system unless they...registered
    videos_checked_out_count = db.Column(db.Integer)

    def to_json(self):
        if self.register_at:
            check_registration = True
        else:
            check_registration = False
        
        return {
            "id": self.customer_id,
            "name": self.name,
            "phone": self.phone_number,
            "postal_code": self.postal_code,
            "registered_at": check_registration,
            "videos_checked_out_count": self.videos_checked_out_count # took cue from postman tests. may need to remove...
            }