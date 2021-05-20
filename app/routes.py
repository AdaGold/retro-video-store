from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
import requests
import os

customers_bp = Blueprint("customer", __name__, url_prefix="/customers")
videos_bp = Blueprint("vidoe", __name__, url_prefix="/videos")

####################################################################
#                              CUSTOMERS ROUTES                        #
####################################################################

@customers_bp.route("", methods=["GET"])
def handle_all_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.get_customer_data_structure())
    return make_response(jsonify(customers_response), 200)

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    try:
        new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.get_customer_data_structure(), 201)
    except TypeError as err:
        return make_response({"details":f"Invalid data: {err}"}, 400)

@customers_bp.route("/<id>", methods=["GET"])
def get_customer():
    customer = Customer.query.get_or_404(id)
    return make_response(customer.get_customer_data_structure(), 200)

""" 
@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == "GET":
        return make_response(goal.goal_data_structure(), 200)
    elif request.method == "PUT":
        goal_data = request.get_json()
        goal.title = goal_data["title"]
        db.session.commit()
        return make_response(goal.goal_data_structure(), 200)
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit() 
        goal_response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
        return make_response(goal_response, 200)
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goal_tasks(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == "GET":
        # Method that appends full task info
        return make_response(goal.tasks_data_structure(), 200)
    if request.method == "POST":
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id
            db.session.commit()
        return make_response({"id": goal.goal_id, "task_ids": request_body["task_ids"]}, 200)

 """