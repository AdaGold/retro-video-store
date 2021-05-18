# from flask import current_app
# from app import db
# from datetime import datetime

# Rentals = db.Table('Rentals',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('customer_id', db.Integer, db.ForeignKey('Customer.id')),
#     db.Column('video_id', db.Integer, db.ForeignKey('Video.id')),
#     db.Column('rental_start', db.DateTime))