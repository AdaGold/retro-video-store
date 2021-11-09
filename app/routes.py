from app import db
from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models.video import Video

video_bp = Blueprint("videos", __name__, url_prefix=("/videos"))
#within the empty quotes for the route do I need to put "/<video>"
@video_bp.route("", methods=["POST"])
def post_video():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
                    return{
                        "details": "invalid data"
                    }, 400

db.session.add()
db.session.commit()

@video_bp.route("", methods=["GET"])
def get_video():
#list = []
 for video in list:
            ({
            "id": video.video_id,
            "title": video.title,
            "release_date": datetime.now(),
            "total_inventory": video.total_inventory
            })

@video_bp.route("/video/<id>",methods=["GET"])
# Gives back details about specific video 
# in the store's inventory.
#response 
                ({
            "id": video.video_id,
            "title": video.title,
            "release_date": datetime.now(),
            "total_inventory": video.total_inventory
            })

@video_bp.route("/video<id>",methods=["PUT"])
#this will update/replace the video id 
#should it return the same as 35-40 as above

