from flask import current_app
from app import db
from sqlalchemy import DateTime

association_table = db.Table('association',
    db.Column('left_id', db.Integer, db.ForeignKey('left.customer_id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.video_id'))
)

class Customer(db.Model):
    __tablename__ = 'left'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos = db.relationship(
        "Video",
        secondary=association_table,
        back_populates="customers")

class Video(db.Model):
    __tablename__ = 'right'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)

    customers = db.relationship(
        "Customer",
        secondary=association_table,
        back_populates="videos")