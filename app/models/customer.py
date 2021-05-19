from app import db
from dataclasses import dataclass
import datetime

@dataclass 
class Customer(db.Model): 
    id: int
    name: str
    registered_at: datetime
    postal_code: str
    phone: str
    videos_checked_out_count: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable = True) 
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0, nullable = True)
    # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)

    def to_dictionary(self):
        '''
        Outputs a dictionary format of the customer object
        '''
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count,
            "registered_at": self.registered_at
            }

        # if self.video_id:
        #     return {
        #         "id": self.id,
        #         "name": self.name,
        #         "postal_code": self.postal_code,
        #         "phone": self.phone,
        #         "videos_checked_out_count": self.videos_checked_out_count,
        #         # "video_id": self.video_id,
        #         "is_registered": self.registered_at != None
        #         }
        # else:
        #     return {
        #         "id": self.id,
        #         "name": self.name,
        #         "postal_code": self.postal_code,
        #         "phone": self.phone,
        #         "videos_checked_out_count": self.videos_checked_out_count,
        #         "is_registered": self.registered_at != None
        #         }
