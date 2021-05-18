from flask import current_app
from app import db

association_table = db.Table('association',
    db.Column('left_id', db.Integer, db.ForeignKey('left.customer_id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.video_id'))
)