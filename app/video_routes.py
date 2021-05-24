from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from dotenv import load_dotenv


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

        return jsonify({"Error": "Enter info for all fields"}), 400

    new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_json_video()), 201

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def handle_video(video_id):

    video = Video.query.get(video_id)

    if request.method == "GET":
        if video is None:
            return jsonify({"Error": f"Video not found"}), 404

        else:
            return jsonify(video.to_json_video()), 200

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):

    video = Video.query.get(video_id)

    if video:
        db.session.delete(video)
        db.session.commit()

        return jsonify({"id": video.id}), 200
    
    else:
        return jsonify({"Error": f"Video {video_id} does not exist"}), 404

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):

    video = Video.query.get(video_id)
    form_data = request.get_json()

    if video: 

        if "title" in form_data.keys() or "release_date" in form_data.keys() or "total_inventory" in form_data.keys():
            
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]

            db.session.commit()
                
            return jsonify(video.to_json_video()), 200

    else: 
        return jsonify({"Error": f"Video {video_id} not relevant"}), 404

@videos_bp.route("/<id>/rentals", methods=["GET"], strict_slashes=False)
def video_customers(id):

    # create instance of video using video id 
    request_body = request.get_json()
    video = Video.query.get(id)
    customers_list = []

    # if video exists
    if video:

        # create join table 
        results = db.session.query(Customer, Video, Rental)\
            .join(Customer, Customer.id==Rental.customer_id)\
                .join(Video, Video.id==Rental.video_id)\
                    .filter(Video.id==id).all()

        for row in results:
            customers_list.append({
                "due_date": row[2].due_date,
                "name": row[0].name,
                "phone": row[0].phone_number,
                "postal_code": row[0].postal_code
            })

        return jsonify(customers_list), 200

    else:
        if video is None:
            return jsonify({"Error": "Video does not exist"}), 404
