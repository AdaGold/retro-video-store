from flask import Blueprint, request, Response, abort, make_response
from app.models.customer import Customer
from .route_utilities import validate_model, create_response_for_model, date_to_str
from datetime import datetime
from ..db import db

bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@bp.post("")
def create_customer():
    request_body = request.get_json()
    request_body["registered_at"] = date_to_str(datetime.now())

    return create_response_for_model(Customer, request_body)

@bp.get("")
def get_customers_with_filters():
    query = db.select(Customer)

    sort_param = request.args.get("sort")
    if sort_param and hasattr(Customer, sort_param):
        query = query.order_by(getattr(Customer, sort_param))
    else:   
        query = query.order_by(Customer.id)

    count_param = request.args.get("count")
    if count_param and count_param.isnumeric():
        count_param = int(count_param) 
    else:
        count_param = None

    customers = None
    if count_param:
        page_param = request.args.get("page_num")
        if page_param and page_param.isnumeric():
            page_param = int(page_param) 
        else:
            page_param = 1

        page = db.paginate(query, page=page_param, per_page=count_param)
        customers = page.items

    else:
        customers = db.session.scalars(query)

    customers_response = [customer.to_dict() for customer in customers]
    return customers_response

@bp.get("/<customer_id>")
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@bp.put("/<customer_id>")
def update_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()

    try:
        customer.update_customer(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    except TypeError as error:
        response = {"message": f"Invalid request: wrong data type {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.commit()
    return Response(status=204, mimetype="application/json") # 204 No Content

@bp.delete("/<customer_id>")
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    for rental in customer.rentals:
        db.session.delete(rental)

    db.session.delete(customer)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.get("/<customer_id>/rentals")
def get_customer_rentals(customer_id):
    customer = validate_model(Customer, customer_id)
    current_rentals = customer.get_active_rentals_data()
    return current_rentals