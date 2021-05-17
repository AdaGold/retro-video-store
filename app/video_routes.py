from app import db
from .models.customer_video import Customer, Video
#from .models.video import Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

#WAVE 1 CURD /CUSTOMERS

video_bp = Blueprint("videos", __name__, url_prefix="/videos")