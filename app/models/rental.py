# from app import db

# class Rental(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
#     video_id = db.Column(db.Integer, db.ForeignKey('vedio.id'), primary_key=True)
#     due_date = db.Column(db.DateTime)
#     customer = db.relationship("Customer", back_populates="videos")
#     video = db.relationship("Video", back_populates="customers")