from app import db 
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from datetime import datetime
import os 
# import requests



retro_video_store_bp = Blueprint("Customer",__name__)

@retro_video_store_bp.route("/customers", methods=["GET"])
def retrieve_all_customers(): 
    customers = Customer.query.all()
    if customers is None: 
        return make_response("",200)
    else: 
        response = [customer.as_json() for customer in customers]
        return make_response(jsonify(response), 200)

@retro_video_store_bp.route("/customers", methods=["POST"])
def create_a_customer(): 
    request_body = request.get_json()

        
    for customer_attribute in ["name","postal_code","phone"]:
        if customer_attribute not in request_body:
            return jsonify(f'Missing required: {customer_attribute}'),400

     

    new_customer = Customer.from_json(request_body)
   
    db.session.add(new_customer)
    db.session.commit()


    response = {
             "id": new_customer.id 

               }
    return make_response(jsonify(response), 201)

@retro_video_store_bp.route("/customers/<customer_id>", methods=["GET","PUT","DELETE"])
def retrieve_one_customer(customer_id): 
    customer = Customer.query.filter_by(id = customer_id).first()

    if customer is None: 
        return make_response("", 404)

    if request.method == "GET":   
        return jsonify({
                "customer": customer.as_json()
        }) 
    elif request.method == "PUT": 
        form_data = request.get_json()

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]


        db.session.commit()
        
        return jsonify({customer.as_json()
        })

#     elif request.method == "DELETE":
#         db.session.delete(customer)
#         db.session.commit()
#         return jsonify (
#         {
#             "details": (f{task.id} "{task.title}" successfully deleted')
#         })
                
    




# video_bp = Blueprint("videos", __name__, url_prefix="/videos")
# @videos_bp.route("", methods=["POST"])
# def create_a_video(): 
#     request_body = request.get_json()

#     if not ("title" in request_body):        
#          return make_response(jsonify({
#             "details": "Invalid data"
#         }), 400)
        

#     new_goal = Goal(title=request_body["title"])
        
#     db.session.add(new_goal)
#     db.session.commit()


#     response = {
#             "goal": new_goal.to_json()
#         }
#     return make_response(jsonify(response), 201)

# @goals_bp.route("", methods=["GET"])
# def retrieve_all_goals():
  
#     if "sort" in request.args and request.args["sort"] == "title": 
#     # if "sort" in request.args == "title": # always false, because it reduces to `if True == "title"`
#         goals = Goal.query.order_by(Goal.title.asc()).all()
    
#     else: 
#         goals = Goal.query.all()

#     return jsonify([goal.to_json() for goal in goals])




# @goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
# def retrieve_one_goals_tasks(goal_id): 
#     goal = Goal.query.filter_by(goal_id=goal_id).first()

#     if goal is None: 
#         return make_response("", 404)
    
#     if request.method == "GET":
#        return jsonify(
#             {"goal":goal.to_json() }
#         )

#     elif request.method == "PUT": 
#         form_data = request.get_json()

#         goal.title = form_data["title"]
    
#         db.session.commit()
        
#         return jsonify({ "goal": goal.to_json() })

#     elif request.method == "DELETE":
#         db.session.delete(goal)
#         db.session.commit()
#         return jsonify (
#         {
#             "details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
#         })


# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def send_task_ids_goal(goal_id): 
  

#     request_body = request.get_json()
#     task_ids = request_body['task_ids']
#     for task_id in task_ids:
#         task = Task.query.filter_by(id = task_id).first()
#         task.goal_id = goal_id

#     db.session.commit()
#     response = {
#                 "id": int(goal_id),
#                 "task_ids": task_ids,
#             }
#     return make_response(jsonify(response), 200)

# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def retrieve_one_task(goal_id): 
#     goal = Goal.query.filter_by(goal_id=goal_id).first()
#     tasks = Task.query.filter_by(goal_id=goal_id).all()
    
#     if goal is None: 
#         return make_response("", 404)


#     response = goal.to_json() # creates a dictionary with id and title entries
#     response["tasks"] = [task.as_json() for task in tasks] # adds a third entry to that dictionary



#     return make_response(jsonify(response), 200)
    
