from flask import current_app
from app import db
from app.models.customer_video_join import association_table  


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