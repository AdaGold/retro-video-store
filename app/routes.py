from app import db
from flask import Blueprint
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from flask import request
from flask import jsonify, make_response
from sqlalchemy import asc, desc 
import requests
import os

# creating instance of the model, first arg is name of app's module
customer_bp = Blueprint("customers", __name__, url_prefix="/customers") # details

#create a customer with null completed at
@customer_bp.route("", methods = ["POST"], strict_slashes = False)
def create_customer():
    try:
        request_body = request.get_json()
        new_customer = Customer.from_json_to_customer(request_body)
        db.session.add(new_customer) # "adds model to the db"
        db.session.commit() # commits the action above
        return jsonify(id = new_customer.id), 201
    except KeyError:
        return {"details": "Bad Request"}, 400
        # return "Bad Request", 400


# Retrieve all /customers  
@customer_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_customers_data():
    customers = Customer.query.all() 
    customers_response = []

    if customers != None:  
        
        customers_response = [customer.customer_to_json_response() \
                for customer in customers]
    return jsonify(customers_response), 200

# Retrieve one /customers/1     
@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes = False)
def retrieve_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer != None:
        return customer.customer_to_json_response(), 200
        # response = customer.customer_to_json_response()
        # if customer.goal_id:
        #     response['task']['goal_id'] = customer.goal_id
        # return response, 200
    return make_response('Not Found', 404)

#Update a customer
@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes = False)  
def update_customer(customer_id):
    customer = Customer.query.get(customer_id) #SQL ALCHEMY QUERY?
    if customer: # if successful quering customer with given customer_id
        form_data = request.get_json()
        if not "name" in form_data or not "postal_code" in form_data \
            or not "phone" in form_data:
            return jsonify("Bad Request"), 400

        # if "name" in form_data: 
        customer.name = form_data["name"]
        # if "postal_code" in form_data:
        customer.postal_code = form_data["postal_code"]
        # if "phone" in form_data:
        customer.phone = form_data["phone"]
        
        db.session.commit() # commiting changes to db
        return customer.customer_to_json_response(), 200

    return jsonify("Not Found"), 404

# Delete a customer
@customer_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes = False)
def customer_task(customer_id):  
    customer = Customer.query.get(customer_id) 
    if customer != None:
        db.session.delete(customer)
        db.session.commit()
        details_str = f"Customer {customer_id} \"{customer.name}\" successfully deleted"
        return jsonify(id = customer.id, detais = details_str), 200
        # return jsonify(id = customer.id), 200

    return jsonify("Not Found"), 404








## TASK / GOAL ROUTES ----------------------------------------------

# creating instance of the model, first arg is name of app's module
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

#create a task with null completed at
@task_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_json_to_task(request_body)
        db.session.add(new_task) # "adds model to the db"
        db.session.commit() # commits the action above
        return new_task.to_json_response(), 201
    except KeyError:
        return {"details": "Invalid data"}, 400

# Retrieve all /tasks  asc, desc, or id asc
@task_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_tasks_data():
    tasks = Task.query.all() 
    sort_by = request.args.get("sort") # query parameters 
    tasks_response = []

    if tasks != None: 
        if sort_by == "asc":  
            # this is a list (queried by title) in asc order
            tasks = Task.query.order_by(Task.title.asc()).all() 

        elif sort_by == "desc":
            # this is a list (queried by title) in desc order
            tasks = Task.query.order_by(Task.title.desc()).all() 
        
        elif sort_by == "id":
            # list, queried by id in asc order:
            tasks = Task.query.order_by(Task.id.asc()).all()  
        
        tasks_response = [task.task_to_json_response() \
                for task in tasks]
    return jsonify(tasks_response), 200

# Retrieve one /task/1     
@task_bp.route("/<task_id>", methods=["GET"], strict_slashes = False)
def retrieve_single_task(task_id):
    task = Task.query.get(task_id)
    if task != None:
        # return task.to_json_response(), 200
        response = task.to_json_response()
        if task.goal_id:
            response['task']['goal_id'] = task.goal_id
        return response, 200
    return make_response('', 404)

#Update a task
@task_bp.route("/<task_id>", methods=["PUT"], strict_slashes = False)  
def update_task(task_id):
    task = Task.query.get(task_id)
    if task: # if successful quering task with given task_id
        form_data = request.get_json()
        if "title" in form_data:
            task.title = form_data["title"]
        if "description" in form_data:
            task.description = form_data["description"]
        if "completed_at" in form_data:
            task.completed_at = form_data["completed_at"]
        db.session.commit() # commiting changes to db
        return task.to_json_response(), 200
    return make_response(""), 404

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"], strict_slashes = False)
def delete_task(task_id):  
    task = Task.query.get(task_id) 
    if task != None:
        db.session.delete(task)
        db.session.commit()
        details_str = f"Task {task_id} \"{task.title}\" successfully deleted"
        return jsonify(details = details_str), 200
    return make_response(""), 404

# Modify part of a task to mark complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes = False)  
def patch_task_mark_complete(task_id):
    task = Task.query.get(task_id)
    # PATCHing if: arg mark_complete specified # in URL and task id 
    # provided exists in database
    if task:                         
        # then call function that changes it to complete
        task.set_completion() # updates it with a date in "completed_at" field
        call_slack(task) # insert post for slack here
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

def call_slack(task):
    '''helper function that posts message to slack'''
    API_KEY = os.environ.get("SLACK_BOT_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    slack_str = f"Someone just completed the task {task.title}"
    # comes from postman body # ID of the channel you want to send the message to
    channel_id = "C0211KC1QSK"
    requests.post(url, data={"token": API_KEY, "channel": channel_id, \
        "text": slack_str})

# Modify part of a task to mark incomplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes = False)  
def patch_task_mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

# GOAL ROUTES start here 
@goal_bp.route("", methods = ["POST"], strict_slashes = False)
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal) # "adds model to the db"
        db.session.commit() # does the action above
        return new_goal.goal_to_json_response(), 201
    except KeyError:
        return {"details": "Invalid data"}, 400

#Retrieve all /goals 
@goal_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_goals_data():
    goals = Goal.query.all() 
    goals_response = []

    if goals != None:
        for goal in goals:
            goals_response.append(goal.simple_response())
    return jsonify(goals_response), 200 ## OR #return goals_response, 200 

# Retrieve one /goal/1     
@goal_bp.route("/<goal_id>", methods=["GET"], strict_slashes = False)
def retrieve_single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal != None:
        return goal.goal_to_json_response(), 200
    return make_response('', 404)

# Delete a goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):  
    goal = Goal.query.get(goal_id) 
    if goal != None:
        db.session.delete(goal)
        db.session.commit()
        details_str = f"Goal {goal_id} \"{goal.title}\" successfully deleted"
        return jsonify(details = details_str), 200    
    return make_response(""), 404

# Update a goal
@goal_bp.route("/<goal_id>", methods=["PUT"], strict_slashes = False)  
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal: # successful updating goal
        form_data = request.get_json() # save user input form_data as json format 
        goal.title = form_data["title"] # updating model
        db.session.commit()
        return goal.goal_to_json_response(), 200
    return make_response(""), 404


# ONE TO MANY RELATIONSHIP - /goals/<goal_id>/tasks - routes
@goal_bp.route("/<goal_id>/tasks", methods = ["POST"], strict_slashes = False)
def post_task_ids_to_goal(goal_id):
    try: 
        request_body = request.get_json()  
        goal = Goal.query.get(goal_id)  # instance of this goal_id including 
                                        # the task ids
        # store list of tasks given in the request body (task_ids)
        task_ids = request_body["task_ids"]  # task_ids - list ie. [1,3,4]
        for task_id in task_ids:
            task = Task.query.get(task_id)  
            # appending those tasks queried into goal with given id
            goal.tasks.append(task) # instance goal with list of
            db.session.commit()
        # display this info into response as json and integers not strings
        return {"id": int(goal_id), "task_ids": task_ids},200
    except:
        return make_response(""), 404 ## not found

@goal_bp.route("/<goal_id>/tasks", methods = ["GET"], strict_slashes = False)
def getting_tasks_of_one_goal(goal_id):
    goal = Goal.query.get(goal_id) 
    if goal: 
        tasks = goal.tasks
        # create a list of tasks and each task CALL FUNCTION task.task_to_json_response()
        new_list = [task.task_to_json_response_w_goal() for task in tasks]
        return {"id": goal.goal_id,
            "title": goal.title,
            "tasks": new_list}, 200
    # if goal doesn't exist
    return make_response(""), 404
