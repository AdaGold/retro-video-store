from app import db
from flask import Blueprint, request, jsonify
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def add_video():
    body = request.get_json() 
  
    if ("title" not in body.keys() or
        "release_date" not in body.keys() or
        "total_inventory" not in body.keys()):
        return {"error" : "Invalid data"}, 400

    new_video = Video(title = body["title"],
                    release_date = body["release_date"],
                    total_inventory = body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return {
        "id": new_video.video_id
    },201


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    title_from_url = request.args.get("title")

    if title_from_url:
        videos = Video.query.filter_by(title = title_from_url)
    
    videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.to_json())

    return jsonify(videos_response), 200


def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_video_by_id(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return ("", 404)
    
    if not is_int(video_id):
        return ("", 400)
    
    return video.to_json(), 200
