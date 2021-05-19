from app import db, helper
#from .models.customer import Customer
from .models.video import Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

#WAVE 1 CRUD / VIDEO

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#GET ALL VIDEOS
@video_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    
    videos = Video.query.all()
    
    video_response =[]
    for video in videos:
        video_response.append(video.video_details())
        
    return jsonify(video_response), 200


#GET video with specific ID
@video_bp.route("/<id>", methods=["GET"], strict_slashes=False)
def get_specific_video(id):
    
    if not helper.is_int(id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    video =  Video.query.get(id)
    
    if video == None:
        return Response ("" , status=404)
    
    if video:
        return make_response(video.video_details(), 200)
    

#POST /video details
@video_bp.route("", methods=["POST"], strict_slashes=False)
def add_videos():
    
    request_body = request.get_json()
    
    if ("title" not in request_body or 
        "release_date" not in request_body or 
        "total_inventory" not in request_body):
        
        return jsonify(details="Bad request"),400
    
    new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
    
    db.session.add(new_video)
    db.session.commit()
    
    return make_response(jsonify(id=new_video.video_id) ,201)


#PUT update a customer detail
@video_bp.route("<id>", methods=["PUT"], strict_slashes=False)
def update_video(id):
    
    video = Video.query.get(id)
    
    if video == None or not video:
        return Response("", status=404)
    

    form_data = request.get_json()
    
    if not form_data or not form_data["title"] or not form_data["release_date"] or not form_data["total_inventory"]:
        return Response("", 400)
    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]
    
    db.session.commit()
    
    return video.video_details(), 200
    

#DELETE a video
@video_bp.route("<id>", methods=["DELETE"], strict_slashes=False)
def delete_video(id):
    
    video = Video.query.get(id)
    
    if video == None:
        return Response("", status=404)
    
    if video:
        db.session.delete(video)
        db.session.commit()
        
        return jsonify(id=int(id)), 200
    
#WAVE 2 - GET /customers/<id>/rentals
@video_bp.route("/<id>/rentals", methods=["GET"], strict_slashes=False)
def get_customers_with_videos(id):
    pass


#OPTIONAL ENHANCEMENTs 
#GET /videos/<id>/history
