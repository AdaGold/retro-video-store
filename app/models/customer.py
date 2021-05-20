from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0, nullable=True)

    def to_json(self):
        """
        Outputs formatted JSON dictionary of customer attributes
        """
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
            }

    def from_json(self, input_data):
        """
        Converts JSON input data into new instance of Customer
        """
        return self(name=input_data["name"],
        postal_code=input_data["postal_code"],
        phone=input_data["phone"])
