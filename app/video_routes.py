from app.models.video import Video
from flask import Blueprint, request
from flask.json import jsonify
from app import db

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    videos = Video.query.all()
    response_body =[video.video_to_json() for video in videos]
    return jsonify(response_body), 200

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_video():
    new_video_data = request.get_json()
    if new_video_data.keys() >= {"title", "release_date", "total_inventory"}:
        new_video = Video(**new_video_data)
        db.session.add(new_video)
        db.session.commit()
        return new_video.video_to_json(), 201
    return {"details": "Invalid data"}, 400

@videos_bp.route("/<int:video_id>", methods=["GET"], strict_slashes=False)
def get_single_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return {"details": "Invalid ID"}, 404
    return video.video_to_json(), 200

@videos_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):
    update_video_data = request.get_json()
    video = Video.query.get(video_id)
    if not video:
        return {"details": "Invalid ID"}, 404
    elif update_video_data.keys() >= {"title", "release_date", "total_inventory"}:
        video.title = update_video_data["title"]
        video.release_date = update_video_data["release_date"]
        video.total_inventory = update_video_data["total_inventory"]
        db.session.commit()
        return video.video_to_json(), 200
    return {"details": "Invalid data"}, 400

@videos_bp.route("/<int:video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return {"details": "Invalid ID"}, 404
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}, 200

