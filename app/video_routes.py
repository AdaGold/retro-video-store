from flask import Blueprint
from flask import request, Blueprint, make_response, jsonify, abort
from app.models.video import Video
from app import db

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=['GET', 'POST'])
def handle_videos():
    VIDEOS = Video.query.all()
    REQUEST_BODY = request.get_json()

    if VIDEOS == None:
        return("", 404)

    elif request.method == 'GET': 
        videos_list = [video.v_json_response() for video in VIDEOS]
        return jsonify(videos_list)
    

    elif request.method == 'POST':
        if "title" not in REQUEST_BODY or \
            "release_date" not in REQUEST_BODY or \
            "total_inventory" not in REQUEST_BODY:
                return {"error" : "Invalid data"}, 400

        new_video = Video(title_of_video = REQUEST_BODY["title"],
                        release_date = REQUEST_BODY["release_date"],
                        total_inventory = REQUEST_BODY["total_inventory"])
            
        db.session.add(new_video)
        db.session.commit()
        return {"id": new_video.video_id}, 201

        

@videos_bp.route("/<video_id>", methods=['GET', 'PUT', 'DELETE'])
def handle_video_by_id(video_id):

    VIDEOS_BY_ID = Video.query.get(video_id)
    UPDATE = request.get_json()


    if VIDEOS_BY_ID == None:
            return ("", 404)

    else:
    
        if request.method == 'GET':
            return jsonify(VIDEOS_BY_ID.v_json_response()), 200


        elif request.method == 'PUT':
            VIDEOS_BY_ID.title_of_video = UPDATE["title"]
            VIDEOS_BY_ID.release_date = UPDATE["release_date"]
            VIDEOS_BY_ID.total_inventory = UPDATE["total_inventory"]
            db.session.add(VIDEOS_BY_ID)
            db.session.commit()
            return jsonify(VIDEOS_BY_ID.v_json_response()), 200
                

            

        elif request.method == 'DELETE':
            db.session.delete(VIDEOS_BY_ID)
            db.session.commit()
            return {"id": VIDEOS_BY_ID.video_id}, 200
            
