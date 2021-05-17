from flask import Blueprint
from app.models.Videos import Video 
from app.models.Customers import Customer
from flask import Blueprint, make_response, jsonify, request
from app import db 
from datetime import date
import requests 
import os 

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")





