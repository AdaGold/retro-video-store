from app import db, helper
from .models.customer_video import Customer, Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

#WAVE 1 CURD / VIDEO

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#GET ALL VIDEOS
