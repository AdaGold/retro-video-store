from flask import Blueprint, request, jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

######################## HELPER FUNCTIONS ######################## 

def invalid_registration_request(request_body):
    if (not request_body
            or "name" not in request_body
            or "postal_code" not in request_body
            or "phone" not in request_body):
        return True

def invalid_video_request(request_body):
    if (not request_body
            or "title" not in request_body
            or "release_date" not in request_body
            or "total_inventory" not in request_body):
        return True

def invalid_checkout_checkin(request_body):
    if (not request_body
            or "customer_id" not in request_body
            or "video_id" not in request_body
            or not isinstance(request_body["customer_id"], int)
            or not isinstance(request_body["video_id"], int)):
        return True
        
######################## CUSTOMER ENDPOINTS ######################## 

@customers_bp.route("/", methods = ["POST"], strict_slashes=False)
def register_customer():
    request_body = request.get_json()
    if invalid_registration_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(id=new_customer.id), 201

@customers_bp.route("/", methods = ["GET"], strict_slashes=False)
def view_all_customers():
        customers = Customer.query.all()
        all_customers = [customer.to_json() for customer in customers]
        return jsonify(all_customers)

@customers_bp.route("/<int:customer_id>", methods = ["GET"], strict_slashes=False)
def view_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_json())

@customers_bp.route("/<int:customer_id>", methods = ["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify(id=customer.id)

@customers_bp.route("/<int:customer_id>", methods = ["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    request_body = request.get_json()
    if invalid_registration_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    customer.name=request_body["name"]
    customer.postal_code=request_body["postal_code"]
    customer.phone=request_body["phone"]
    db.session.commit()
    return jsonify(customer.to_json())

@customers_bp.route("/<int:customer_id>/rentals", methods = ["GET"], strict_slashes=False)
def view_customer_rentals(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_rentals = []
    for rental in customer.videos:
        video = Video.query.get(rental.video_id)
        movie_details = {"release_date":video.release_date,
                "title": video.title,
                "due_date": rental.due_date}
        customer_rentals.append(movie_details)
    return jsonify(customer_rentals), 200

######################## VIDEO ENDPOINTS ######################## 

@videos_bp.route("/", methods = ["POST"], strict_slashes=False)
def register_video():
    request_body = request.get_json()
    if invalid_video_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"],
                        available_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return jsonify(id=new_video.id), 201

@videos_bp.route("/", methods = ["GET"], strict_slashes=False)
def view_all_videos():
    videos = Video.query.all()
    all_videos = [video.to_json() for video in videos]
    return jsonify(all_videos)

@videos_bp.route("/<int:video_id>", methods = ["GET"], strict_slashes=False)
def view_video(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify(video.to_json())

@videos_bp.route("/<int:video_id>", methods = ["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify(id=video.id)

@videos_bp.route("/<int:video_id>", methods = ["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    request_body = request.get_json()
    if invalid_video_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    video.title=request_body["title"]
    video.release_date=request_body["release_date"]
    video.total_inventory=request_body["total_inventory"]
    db.session.commit()
    return jsonify(video.to_json())

@videos_bp.route("/<int:video_id>/rentals", methods = ["GET"], strict_slashes=False)
def view_customer_rentals(video_id):
    video = Video.query.get_or_404(video_id)
    video_rentals = []
    for rental in video.customers:
        customer = Customer.query.get(rental.customer_id)
        customer_details = {"due_date": rental.due_date,
                            "name": customer.name,
                            "phone": customer.phone,
                            "postal_code": customer.postal_code}
        video_rentals.append(customer_details)
    return jsonify(video_rentals)

######################## RENTAL ENDPOINTS ######################## 

@rentals_bp.route("/check-out", methods = ["POST"], strict_slashes=False)
def checkout():
    request_body = request.get_json()
    if invalid_checkout_checkin(request_body):
        return jsonify(details=f"Invalid data"), 400
    new_rental = Rental(customer_id = request_body["customer_id"],
                        video_id = request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    customer.videos_checked_out_count += 1
    video = Video.query.get(request_body["video_id"])
    if not video.available_inventory:
        return jsonify(details=f"Video not available"), 400
    video.available_inventory -= 1
    db.session.add(new_rental)
    db.session.commit()
    rental_response = new_rental.to_json()
    rental_response["due_date"] = new_rental.due_date
    return jsonify(rental_response)

@rentals_bp.route("/check-in", methods = ["POST"], strict_slashes=False)
def checkin():
    request_body = request.get_json()    
    if invalid_checkout_checkin(request_body):
        return jsonify(details=f"Invalid data"), 400
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    rental = Rental.query.filter_by(video_id=video.id, customer_id=customer.id).first()
    if rental:
        customer.videos_checked_out_count -= 1
        video.available_inventory += 1
        db.session.delete(rental)
        db.session.commit()
        return jsonify(rental.to_json())
    return jsonify(details=f"Invalid data"), 400