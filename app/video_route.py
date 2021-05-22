from app import db
from app.models.video import Video
from flask import request, Blueprint, make_response,jsonify
from datetime import datetime 


# Video route for all inquiry GET & POST
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET", "POST"])
def handle_video_get_post_all():

    if request.method == "GET":

        video_list = Video.query.all()
        video_response = []
        
        if video_list is None:
            return make_response("", 404)
        
        

        for video in video_list:

            video_response.append(video.json_object())
        return jsonify(video_response)
    
    elif request.method == "POST":

        request_body = request.get_json()
        
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({
                "details": "Invaild data"
            }), 400
            
        new_video = Video(title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        
        return (
            {
            "id": new_video.video_id

        }, 201)



@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_video(video_id):
    video = Video.query.get(video_id)
    #when I request in the url and have no details return None and a 404 message
    
    if video is None: #If customer 
        return jsonify(None), 404

    if request.method == "GET":

        return make_response(video.json_object(), 200)

    elif request.method == "PUT":
        request_body = request.get_json()

        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({
                "details": "Invaild data"
            }), 400

        form_data = request.get_json()
        
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"] 

        db.session.commit()

        return make_response(video.json_object())

    elif request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()
    return make_response({
        "id": video.video_id

    }, 200)
    
