from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.video import Video

load_dotenv()

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods = ["GET"])
def get_videos():
    '''gets all videos from database'''
    videos_query = Video.query.all()

    return make_response(jsonify([Video.build_dict() for video in videos_query]))

@videos_bp.route("/<id>", methods = ["GET"])
def get_video(id):
    '''gets one video'''
    video = Video.query.get_or_404(id)

    return make_response({"video": video.build_dict()}, 200)

@videos_bp.route("", methods = ["POST"])
def add_videos():
    '''adds videos'''
    request_body = request.get_json()
    if "title" not in request_body.keys() or "release_date" not in request_body.keys() or "total_inventory" not in request_body.keys():
        return make_response({"details": "insufficient data"})
    new_video = Video(
        title = request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"]
    )
    db.session.add(new_video)
    db.session.commit()

    return make_response({"video": new_video.build_dict()}, 201)

@videos_bp.route("/<id>", methods = ["PUT"])
def update_videos(id):
    '''updates a video '''
    video = Video.query.get_or_404(id)
    form_data = request.get_json()

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]

    db.session.commit()

    return make_response({"video": video.build_dict()}, 200)

@videos_bp.route("/<id>", methods = ["DELETE"])
def delete_video(id):

    video = Video.query.get_or_404(id)
    db.session.delete(video)
    db.session.commit()

    return make_response({"details" : f"Video {video.title} has been deleted"})