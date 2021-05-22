from app import db
from dataclasses import dataclass
import datetime

@dataclass
class Rental(db.Model):
    id: int
    customer_id: int
    video_id: int
    check_out: datetime
    due_date: datetime
    check_in: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    check_out = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    check_in = db.Column(db.DateTime, nullable = True)

    def to_dictionary(self):
        '''
        Outputs a dictionary format of the video object
        '''
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
        }