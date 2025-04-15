from flask import Blueprint
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
