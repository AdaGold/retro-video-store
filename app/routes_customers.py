from flask import Blueprint, request, jsonify, make_response
from app import db 

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
