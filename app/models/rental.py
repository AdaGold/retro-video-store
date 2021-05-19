from flask import current_app
from app import db
# from app.models.customer import Customer
# from app.models.video import Video

# from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# association_table = Table('association', Base.metadata,
#     Column('customer_id', Integer, ForeignKey('customer.id')),
#     Column('video_id', Integer, ForeignKey('video.id'))
# )

class CustomerVideoRental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)

    # left = relationship('Left', backref=backref('right_association'))
    # right = relationship('Right', backref=backref('left_association'))