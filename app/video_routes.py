from flask import Blueprint
from flask import request, Blueprint, make_response, jsonify, abort
from app.models.video import Video
from app import db

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=['GET', 'POST'])
def handle_videos():

    if request.method == 'GET':

        video = Video.query.all()
        
        videos = []

        for video in videos:
            videos.append(video.to_json())
        
        db.session.commit()
        return jsonify(videos), 200
    
    
    if request.method == 'POST':
        request_body = request.get_json()

        if "title" not in request_body or \
            "release_date" not in request_body or \
            "total_inventory" not in request_body:
                return ("", 400)
        
        else:
            new_video = Video(title_of_video = request_body["title"],
                                release_date = request_body["release_date"],
                                total_inventory = request_body["total_inventory"])
            
            db.session.add(new_video)
            db.session.commit()

            return {"id": new_video.video_id}, 201

        

@videos_bp.route("/<video_id>", methods=['GET', 'PUT', 'DELETE'])
def handle_video_by_id(video_id):

    video = Video.query.get(video_id)


    if video == None:
            return ("", 404)

    else:
    
        if request.method == 'GET':
            return jsonify(video.v_json_response()), 200


        elif request.method == 'PUT':
            update = request.get_json() 

            video.title_of_video = update["title"]
            video.release_date = update["release_date"]
            video.total_inventory = update["total_inventory"]

            db.session.commit()
            return jsonify(video.v_json_response()), 200
                

            

        elif request.method == 'DELETE':
            db.session.delete(video)
            db.session.commit()
            return {"id": video.video_id}
            
