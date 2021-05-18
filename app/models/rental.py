from flask import current_app
from app import db


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)