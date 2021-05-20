from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, jsonify, Response, make_response
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    if "name" in request_body.keys() and "postal_code" in request_body.keys() and "phone" in request_body.keys() :
        customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"], 
                    phone=request_body["phone"]
                    )
        customer.created=datetime.now()
        db.session.add(customer)
        db.session.commit()
        return jsonify({"id": customer.id}), 201
    else:
        return make_response(
            {"details": "Invalid data"
            }
        ), 400

@customers_bp.route("", methods=["GET"])
def get_customers():
    request_body = request.get_json()
    customers = Customer.query.all()
    customers_response = [customer.api_response() for customer in customers] 
    return jsonify(customers_response), 200

@customers_bp.route("/<id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return make_response(jsonify(None), 404)
    return jsonify(customer.api_response()), 200
    # return jsonify({"customer": customer.api_response()}), 200

@customers_bp.route("/<id>", methods=["PUT"])
def put_customer(id):
    customer = Customer.query.get(id)
    form_data = request.get_json()
    if customer is None:
            return Response(None),404 
    if "name" in form_data.keys() and "postal_code" in form_data.keys() and "phone" in form_data.keys() :
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        db.session.commit()     
        return jsonify(customer.api_response()), 200 
        # return jsonify({"customer": customer.api_response()}), 200 
    return make_response(
            {"details": "Invalid data"
            }
        ), 400    

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return Response(None),404
    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"id": customer.id
        }
    ), 200

@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    if "title" in request_body.keys():
        video = Video(title=request_body["title"],
                release_date=request_body["release_date"],
                total_inventory=request_body["total_inventory"],
                    )
        db.session.add(video)
        db.session.commit()
        return jsonify({"id": video.id}), 201
    else:
        return make_response(
            {"details": "Invalid data"
            }
        ), 400

@videos_bp.route("", methods=["GET"])
def get_videos():
    request_body = request.get_json()
    videos = Video.query.all()
    videos_response = [video.api_response() for video in videos] 
    return jsonify(videos_response), 200

@videos_bp.route("/<id>", methods=["GET"])
def get_video(id):
    video = Video.query.get(id)
    if video is None:
        return make_response(jsonify(None), 404)
    return jsonify(video.api_response()), 200

@videos_bp.route("/<id>", methods=["PUT"])
def put_video(id):
    video = Video.query.get(id)
    form_data = request.get_json()
    if video is None:
        return Response(None),404 
    if "title" in form_data.keys() and "release_date" in form_data.keys() and "total_inventory" in form_data.keys() :
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        db.session.commit()     
        return jsonify(video.api_response()), 200 
    return make_response(
            {"details": "Invalid data"
            }
        ), 400  

@videos_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video = Video.query.get(id)
    if video is None:
        return Response(None),404
    db.session.delete(video)
    db.session.commit()
    return make_response(
        {"id": video.id
        }
    ), 200

# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = Task.query.get(task_id)
#     if task is None:
#         return Response(None),404
#     task.completed_at = datetime.now()
#     db.session.commit()
#     slack_bot_complete(task.title)
#     return jsonify({"task": task.api_response()}), 200   #removed "true" as argument

# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = Task.query.get(task_id)
#     if task is None:
#         return Response(None),404
#     task.completed_at = None
#     db.session.commit()
#     return jsonify({"task": task.api_response()}), 200    



#

# @goals_bp.route("", methods=["GET"])
# def get_goals():
#     goals = Goal.query.all()
#     goals_response = [goal.api_response() for goal in goals]
#     return jsonify(goals_response), 200

# @goals_bp.route("/<goal_id>", methods=["GET"])
# def get_goal(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return make_response(jsonify(None), 404)
#     return jsonify({"goal": goal.api_response()}), 200    

# @goals_bp.route("/<goal_id>", methods=["PUT"])
# def put_goal(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return Response(None),404
#     form_data = request.get_json()
#     goal.title = form_data["title"]
#     db.session.commit()
#     return jsonify({"goal": goal.api_response()}), 200 

# @goals_bp.route("/<goal_id>", methods=["DELETE"])
# def delete_goal(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return Response(None),404
#     db.session.delete(goal)
#     db.session.commit()
#     return make_response(
#         {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'
#         }
#     ), 200

# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def post_goal_tasks(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return Response(None),404

#     form_data = request.get_json()
#     for task_id in form_data["task_ids"]:
#         task = Task.query.get(task_id)
#         task.goal_id = goal_id
#         db.session.commit()
#     return make_response({"id": goal.id,
#                     "task_ids": form_data["task_ids"]}), 200

# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_goal_tasks(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return Response(None),404

#     tasks_list = [task.api_response() for task in goal.tasks]

#     response_body = {
#         "id": goal.id,
#         "title": goal.title,
#         "tasks": tasks_list
#         }
#     return (response_body), 200

# def slack_bot_complete(task_title):
#     return requests.post(("https://slack.com/api/chat.postMessage"), {
#         'token': os.environ.get("slackbot_API_KEY"),
#         'channel': "task-notifications",
#         'text': f"Someone just completed {task_title}"
#     }).json()

