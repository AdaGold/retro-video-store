from app import db
from app import helper
from .models.customer import Customer
from .models.video import Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

#WAVE 1 CURD /CUSTOMERS

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

# GET all customers



