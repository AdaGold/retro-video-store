
from flask import Blueprint
from app.models.video import Video
from app import db
from flask import request, Blueprint, make_response, jsonify


video_bp = Blueprint("videos", __name__, url_prefix="/videos")
@video_bp.route("", methods=["GET", "POST"])
def list_videos():  # NameError
# GET /videos
    if request.method == "GET":

        videos = Video.query.all()
        videos_response = []

        for video in videos:
            videos_response.append(video.video_get_json())
        return jsonify(videos_response), 200

# POST /videos
    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()

        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return {
                "details": "Bad Request"    #correct?
            }, 400

        video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"], # Or release_date
            total_inventory=request_body["total_inventory"]
        )

        db.session.add(video)
        db.session.commit()

        return video.video_get_json(), 201 #where video is created?

@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def single_video(video_id):
    video = Video.query.get(video_id)

    if video == None:
        return make_response(f"Video {video_id} not found", 404)

# GET /vidoes/<id>
    if request.method == "GET":
        return video.video_get_json(),200

# PUT /videos/<id>
    elif request.method == "PUT":
        request_body = request.get_json()

        video = Video.query.get(video_id)
        if video == None:
            return make_response(f"Video {video_id} not found"), 404

        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return {
                "details": f"Not found"
            }, 400

        #update customer info
        video.title = request_body["title"]
        video.release_date= request_body["release_date"]
        video.total_inventory= request_body["total_inventory"]
        
        db.session.commit()

        return video.video_get_json(), 200
    
# DELETE /videos/<id>
    elif request.method == "DELETE":
        video = Video.query.get(video_id)
        if video == None:
            return make_response(f"Video {video_id} not found", 404)
        
        db.session.delete(video)
        db.session.commit()

        return {
            "id":int(video_id)
        }, 200
        