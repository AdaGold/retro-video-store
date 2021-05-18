from app import db 
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import os 
# import requests



retro_video_store_bp = Blueprint("Customer",__name__)

@retro_video_store_bp.route("/customers", methods=["GET"])
def retrieve_all_customers(): 
    customers = Customer.query.all()
    if customers is None: 
        return make_response("",200)
    else: 
        response = [customer.as_json() for customer in customers]
        return make_response(jsonify(response), 200)


