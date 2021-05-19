import requests
from app import db
from app.models.video import Video
from app.models.customer import Customer
from flask import request, Blueprint, make_response, jsonify, abort

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# HELPER FUNCTIONS:
#=============================================================================


def valid_id_or_400(input_id):
    """
    input: an input id 
    output: a 400 status code if the input ID is not able to be converted to an integer  
    """
    # tries to convert the input_id to an integer
    try:
        return int(input_id)
    # if a ValueError is raised, an abort with 400 gets triggered 
    except ValueError:
        abort(400,{"message": f"ID {input_id} must be an integer", "success": False})


# CUSTOMERS ENDPOINTS:
#=============================================================================

# For POST and PUT requests, responses with 4XX response codes should also return a response body with some indication of what went wrong.

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_customers():
    
    customers = Customer.query.all()
    cust_response = []

    # ❓ Not actually sure using len() is the best way to do this:
    # The API should return an empty array and a status 200 if there are no customers.
    if len(customers) == 0:
        return make_response("No existing customers in database", 200)

    # ❓ would like to review why this step and why it's necessary - what does each_cust look like (what is its data type) prior to being converted to json? 
    for each_cust in customers:
        cust_response.append(each_cust.convert_to_json())


    return jsonify(cust_response), 200




# @customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
# def get_single_customer(customer_id):
    
#     valid_id_or_400(customer_id)



@customers_bp.route("", methods=["POST"], strict_slashes=False)
def add_new_customer():

    request_body = request.get_json()

    new_customer = Customer(name=request_body["name"], 
                            postal_code=request_body["postal_code"], 
                            phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    return make_response({"id": new_customer.customer_id}, 201)




@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    valid_id_or_400(customer_id)





@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):

    valid_id_or_400(customer_id)






# VIDEOS ENDPOINTS:
#=============================================================================

# For POST and PUT requests, responses with 4XX response codes should also return a response body with some indication of what went wrong.