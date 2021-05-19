# from re import U
# from app import db
# from app.models.customers import Customer
# from app.models.videos import Video
# from flask import request, Blueprint, make_response, jsonify
# from datetime import datetime
# import os, requests

# customers_bp = Blueprint("cumtomers",__name__,url_prefix="/customers")
# videos_bp = Blueprint("videos",__name__,url_prefix="/videos")


# @videos_bp.route("", methods=["POST","GET"], strict_slashes = False)
# def create_videos():

#     if request.method == "POST":
#         request_body = request.get_json()
        
#         if "title" not in request_body:
#             return ({"details":"Invalid data"},400)
#         else:
#             video = Video(title=request_body["title"],
#                         release_date=datetime.utcnow(),
#                         total_inventory =request_body["total_inventory"])
#             db.session.add(video)
#             db.session.commit()

#             return make_response(video.video_to_json(),201)
#     else:
        
#         videos = Video.query.all()

#         videos_response = []
#         for video in videos:
#                 videos_response.append(video.video_to_json())

#         return jsonify(videos_response)


# @customers_bp.route("/<video_id>", methods=["GET","PUT","DELETE","PATCH"], strict_slashes = False)
# def a_single_video(customer_id):
#     video = Video.query.get(customer_id)

#     if video is None:
#         return make_response(" ", 404)
    
#     if request.method == "GET":
#         return make_response(video.video_to_json(),200)

#     elif request.method == "PUT":
#         form_data = request.get_json()
#         video.name = form_data["title"]
#         video.total_inventory = form_data["total_inventory"]
        
#         db.session.commit()

#         return make_response(video.video_to_json(),200)

#     elif request.method == "DELETE":
#         db.session.delete(video)
#         db.session.commit()

#         return make_response({id:video.video_id})