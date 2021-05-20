from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response,jsonify
from datetime import datetime 
import requests
import json



customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customer_bp.route("", methods=["GET", "POST"])
def handle_customer():
    if request.method == "GET":
        
        
        customer_list = Customer.query.all()

            
        customer_response = []

        for customer in customer_list:
        
            customer_response.append(customer.json_object())
        
        return jsonify(customer_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body):
            return make_response({
                "details": "Invalid data"
            }), 400
    
        new_customer = Customer(name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])
        if new_customer.registered_at == None:
            new_customer.registered_at = datetime.now()

        db.session.add(new_customer)
        db.session.commit()

        return make_response({"id": new_customer.customer_id}), 201

        # db.session.add(new_task)
        # db.session.commit()
























# # @customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
# # def get_customer(customer_id):

# #     customer = Customer.query.get(customer_id)

# #     if customer is None:
# #         return jsonify(None), 404

# #     if request.method == "GET":
# #         return jsonify({"goal": goal.goal_json_object()}), 200

# #     elif request.method == "PUT":
# #         form_data = request.get_json()
# #         #Go and get the data from the request 
# #         goal.title = form_data["title"]
        
# #         db.session.commit()
# #         return jsonify({"goal": goal.goal_json_object()}),200

# #     elif request.method == "DELETE":
# #         db.session.delete(goal)
# #         db.session.commit()
        
# #         return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200
