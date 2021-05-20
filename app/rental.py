# from app import db
# from dataclasses import dataclass
# import datetime

# @dataclass
# class Rental(db.Model):
#     id: int
#     customner_id: int
#     video_id: int
#     due_date: datetime

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
#     # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)
#     due_date = db.Column(db.DateTime)

#     def to_dictionary(self):
#         '''
#         Outputs a dictionary format of the video object
#         '''
#         return {
#             "id": self.id,
#             # "customer_id": self.customer_id,
#             # "video_id": self.video_id,
#             "due_date": self.due_date
#         }