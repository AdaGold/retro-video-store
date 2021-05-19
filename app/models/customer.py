from flask import current_app
from app import db

# videos_fk = db.Table('videos_fk',
#     db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
#     db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True)
# )

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), nullable=True)
    videos_checked_out_count = db.Column(db.Integer)
    # video_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    # video_id = db.relationship('Video', secondary='videos', lazy='subquery',backref=db.backref('customers', lazy=True))



    def to_json(self):

        regular_response = {

            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": 0
        }
        return regular_response
