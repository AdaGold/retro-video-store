from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.video import Video
from dotenv import load_dotenv
from datetime import datetime


videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
load_dotenv()

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():

    videos = Video.query.all()
    videos_response = []

    if videos is None:
        return 404

    for video in videos:
        videos_response.append(video.to_json_video())

    return jsonify(videos_response), 200


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def new_video():

    request_body = request.get_json()

    if "title" not in request_body.keys() or "release_date" not in request_body.keys() or "total_inventory" not in request_body.keys():

        error_response = {"errors": "enter info for all fields"}

        return jsonify(error_response), 400

    new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    valid_video = new_video.to_json_video()

    return jsonify(valid_video), 201

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def handle_video(video_id):

    video = Video.query.get(video_id)

    if request.method == "GET":
        if video is None:
            return make_response(f"404 Not Found", 404) 

        else:
            one_video = video.to_json_video()

            return jsonify(one_video)

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):

    video = Video.query.get(video_id)

    if video:
        db.session.delete(video)
        db.session.commit()

        response = {"details": "Video successfully deleted"}

        return jsonify(response), 200
    
    else:
        return make_response(f"Video does not exist", 404)

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):

    video = Video.query.get(video_id)

    if video: 

        form_data = request.get_json()

        print(form_data)

        # customer.name = form_data["name"]
        # customer.phone_number = form_data["phone"]
        # customer.postal_code = form_data["postal_code"]
        # customer.registered_at = datetime.utcnow()
        # db.session.commit()
        
        # if customer.videos_checked_out is None:
        #     customer.videos_checked_out = 0
        #     db.session.commit()

        if video.name != form_data["title"]: 
            video.name = form_data["title"]
            db.session.commit()

            updated_video = video.to_json_video()
            return jsonify(updated_video), 200

        elif video.release_date != form_data["release_date"]:
            video.release_date = form_data["release_date"]
            db.session.commit()

            updated_video = video.to_json_video()
            return jsonify(updated_video), 200

        elif video.total_inventory != form_data["total_inventory"]:
            video.total_inventory = form_data["total_inventory"]
            db.session.commit()
        
            updated_video = video.to_json_video()
            return jsonify(updated_video), 200


        # updated_customer = {
        #         "id": customer.customer_id,
        #         "name": customer.name,
        #         "phone": customer.phone_number,
        #         "postal_code": customer.postal_code,
        #         "registered_at": customer.registered_at,
        #         "videos_checked_out_count": customer.videos_checked_out
        # }


    else: 
        return make_response("", 404) 
