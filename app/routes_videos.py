from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, request, jsonify, make_response
from app import db 

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    videos = Video.query.all() 
    videos_response = [] 

    for video in videos: 
        videos_response.append(video.to_json())

    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = Video.query.get(video_id)
    
    if video: 
        return jsonify(video.to_json()), 200
    
    return make_response("", 404)

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_video(): 
    request_body = request.get_json()
    
    keys = ["title", "release_date", "total_inventory"]
    for key in keys: 
        if key not in request_body:
            return {"details": "Invalid data"}, 400

    new_video = Video.make_a_video(request_body, id=None)

    db.session.add(new_video)
    db.session.commit() 
    return {"id": new_video.video_id},201

@videos_bp.route("<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get(video_id)
    
    if video: 
        update_data = request.get_json() 
        
        keys = ["title", "release_date", "total_inventory"]
        for key in keys: 
            if key not in update_data or bool(update_data) is False:
                return {"details": "Invalid data"}, 400

        db.session.query(Video).filter(Video.video_id==video_id).update(update_data)
        db.session.commit()
        return jsonify(video.to_json()), 200
    
    return make_response("", 404)

@videos_bp.route("<int:video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video: 
        db.session.delete(video)
        db.session.commit()
        
        return {
            "id": video_id
        }, 200 
    
    return make_response("", 404)

@videos_bp.route("<int:video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_from_videos(video_id): 
    video = Video.query.get(video_id)

    if video: 
        rentals = Rental.query.filter_by(video_id=video_id).all()
        rental_list = [] 

        if rentals != None: 
            for rental in rentals: 
                customer = Customer.query.get(rental.customer_id)
                rental_list.append(rental.videos_associated_rentals(customer))
            return jsonify(rental_list), 200
        return jsonify(rental_list), 200 
    
    return make_response("", 404)
