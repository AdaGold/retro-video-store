
from flask import Blueprint
from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask import request, Blueprint, make_response, Response, jsonify
from datetime import date
import requests

video_bp = Blueprint("videos", __name__, url_prefix="/videos")
@video_bp.route("", methods=["GET", "POST"])
def list_videos():  # NameError
# GET /videos
    if request.method == "GET":

        videos = Video.query.all()
        videos_response = []

        for video in videos:
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory":video.total_inventory,
                "availiable_inventory":video.availiable_inventory
                }, 
                {
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory":video.total_inventory,
                "availiable_inventory":video.availiable_inventory 
                })
            #The API should return an empty array and a status 200 if there are no videos.
        return jsonify(videos_response)

# POST /videos
    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()

        if "title" or "release_date" or "total_inventory" not in request_body:
            return {
                "details": "Bad Request"
            }, 400

        video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"], # Or release_date
            total_inventory=request_body["total_inventory"]
        )

        db.session.add(video)
        db.session.commit()

        return {
            "video": {
                "id": video.video_id
            }
        }, 201

@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def single_video(video_id):
    video = Video.query.get(video_id)

    if video == None:
        return make_response(f"Video {video_id} not found", 404)

# GET /vidoes/<id>
    if request.method == "GET":
        return {
            "video": {
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory":video.total_inventory,
                "availiable_inventory":video.availiable_inventory
            }
        },200

# PUT /videos/<id>
    elif request.method == "PUT":
        form_data = request.get_json()

        video.title = form_data["title"]

        db.session.commit()

        return {
            "video": {
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory":video.total_inventory,
                "availiable_inventory":video.availiable_inventory
                }
            }, 200
    
# DELETE /videos/<id>
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
            
        return {
            "details": f"Video {video.video_id} \"{video.title}\" successfully deleted"
        },200