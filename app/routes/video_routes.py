from flask import Blueprint, request, Response, abort, make_response
from app.models.video import Video
from .route_utilities import validate_model, create_model
from datetime import datetime
from ..db import db

bp = Blueprint("videos_bp", __name__, url_prefix="/videos")


@bp.post("")
def create_video():
    request_body = request.get_json()
    return create_model(Video, request_body)

@bp.get("")
def get_all_videos():
    query = db.select(Video)
    videos = db.session.scalars(query.order_by(Video.id))
    videos_response = [video.to_dict() for video in videos]
    return videos_response

@bp.get("/<video_id>")
def get_one_video(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict()

@bp.put("/<video_id>")
def update_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()

    try:
        video.update_video(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    except TypeError as error:
        response = {"message": f"Invalid request: wrong data type {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.commit()
    return Response(status=204, mimetype="application/json") # 204 No Content

@bp.delete("/<video_id>")
def delete_video(video_id):
    video = validate_model(Video, video_id)

    for rental in video.rentals:
        db.session.delete(rental)

    db.session.delete(video)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.get("/<video_id>/rentals")
def get_rentals_by_video(video_id):
    video = validate_model(Video, video_id)

    current_rentals = []
    for rental in video.rentals:
        if rental.status == "RENTED":
            data = {
                "name": rental.customer.name,
                "phone": rental.customer.phone,
                "postal_code": rental.customer.postal_code,
                "due_date": rental.due_date
            }
            current_rentals.append(data)
    
    return current_rentals
