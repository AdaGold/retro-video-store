from app.models.customer import Customer
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
        new_video.available_inventory = new_video_data["total_inventory"]
        db.session.add(new_video)
        db.session.commit()
        return new_video.video_to_json(), 201
    return {"details": "Invalid data"}, 400

@videos_bp.route("/<int:video_id>", methods=["GET"], strict_slashes=False)
def get_single_video(video_id):
    video = Video.query.get_or_404(video_id)
    return video.video_to_json(), 200

@videos_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):
    update_video_data = request.get_json()
    video = Video.query.get_or_404(video_id)
    if update_video_data.keys() >= {"title", "release_date", "total_inventory"}:
        video.title = update_video_data["title"]
        video.release_date = update_video_data["release_date"]
        video.total_inventory = update_video_data["total_inventory"]
        db.session.commit()
        return video.video_to_json(), 200
    return {"details": "Invalid data"}, 400

@videos_bp.route("/<int:video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}, 200

@videos_bp.route("/<int:video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_videos_check_out_by_customer(video_id):
    video = Video.query.get_or_404(video_id)
    video_rental_rec = []
    for rental in video.rentals:
        customer = Customer.query.get(rental.customer_id)
        video_rental_rec.append({"name" : customer.name,
                            "phone" : customer.phone,
                            "postal_code" : customer.postal_code,
                            "due_date" : rental.due_date
                            })
    return jsonify(video_rental_rec), 200