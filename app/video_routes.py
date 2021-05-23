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

        return {"id": video.id}, 200
    
    else:
        return make_response(f"Video {video_id} does not exist", 404)

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
    
            updated_video = video.to_json_video()
            
            return jsonify(updated_video), 200

    else: 
        return make_response(f"Video {video_id} not relevant", 404) 

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
                    .filter(Video.id==Video.id).all()

        unpack_join = results[0]

        customer = unpack_join[0]
        rental = unpack_join[2]

        response = {
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone_number,
            "postal_code": customer.postal_code
        }

        return jsonify(response), 200

    else:
        if video is None:
            return {"Error": "Video does not exist"}, 404
