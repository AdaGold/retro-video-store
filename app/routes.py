from flask import Blueprint
from app import db
from flask import jsonify
from .models.customer import Customer
import os

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")