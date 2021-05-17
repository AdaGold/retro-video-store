from app import db
from flask import Blueprint, request, jsonify
from app.models.customer import Customer
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")