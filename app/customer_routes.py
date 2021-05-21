from flask import Blueprint, request
from flask.json import jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_customers():
    customers = Customer.query.all()
    response_body =[customer.customer_to_json() for customer in customers]
    return jsonify(response_body), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_customer():
    new_customer_data = request.get_json()
    if new_customer_data.keys() >= {"name", "postal_code", "phone"}:
        new_customer = Customer(**new_customer_data)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.customer_to_json()), 201
    return jsonify({"details": "Invalid data"}), 400

@customers_bp.route("/<int:customer_id>", methods=["GET"], strict_slashes=False)
def get_single_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.customer_to_json()), 200

@customers_bp.route("/<int:customer_id>", methods=["PUT"], strict_slashes=False)
def update_single_customer(customer_id):
    update_customer_data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    if update_customer_data.keys() >= {"name", "postal_code", "phone"}:
        customer.name = update_customer_data["name"]
        customer.postal_code = update_customer_data["postal_code"]
        customer.phone = update_customer_data["phone"]
        db.session.commit()
        return jsonify(customer.customer_to_json()), 200
    return jsonify({"details": "Invalid data"}), 400

@customers_bp.route("/<int:customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"id": customer.id}), 200

@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_videos_check_out_by_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_rental_rec = []
    for rental in customer.rentals:
        video = Video.query.get(rental.video_id)
        customer_rental_rec.append({"release_date" : video.release_date,
                            "title" : video.title,
                            "due_date" : rental.due_date
                            })
    return jsonify(customer_rental_rec), 200
