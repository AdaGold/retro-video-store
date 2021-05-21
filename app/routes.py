from flask import Blueprint, request, make_response
from flask import jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import CustomerVideoRental
import datetime
import requests

# class Customer routes
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_customers():

    if request.method == "GET":

        customers = Customer.query.all()

        customer_list = []

        for customer in customers:
            customer_list.append(customer.to_json())

        return jsonify(customer_list)
    
    if request.method == "POST":

        request_body = request.get_json()

        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify({
                "details": "Invalid data.  Missing name, postal code, and/or phone."
            }), 400
        
        new_customer = Customer(name=request_body["name"],
                                postal_code=request_body["postal_code"],
                                phone_num=request_body["phone"],
                                register_at=datetime.datetime.now())
        
        db.session.add(new_customer)
        db.session.commit()

        return new_customer.to_json(), 201


@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return "Customer not found.", 404

    if request.method == "GET":
        return customer.to_json()
    
    if request.method == "PUT":

        customer_data = request.get_json()

        if "name" not in customer_data or "postal_code" not in customer_data or "phone" not in customer_data:
            return jsonify({
                "details": "Invalid data.  Missing name, postal code, and/or phone."
            }), 400

        customer.name = customer_data["name"]
        customer.postal_code = customer_data["postal_code"]
        customer.phone_num = customer_data["phone"]

        db.session.commit()

        return customer.to_json()
    
    if request.method == "DELETE":

        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            "id": customer.id,
            "details": f'Customer {customer.id}: {customer.name} successfully deleted.'
        })

# List customer's rentals
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def handle_customer_rentals(customer_id):

        customer_data = db.session.query(Customer, Video, CustomerVideoRental).join(Customer, Customer.id==CustomerVideoRental.customer_id)\
            .join(Video, Video.id==CustomerVideoRental.video_id).filter(Customer.id == customer_id).all()

        if customer_data is None: 
            return "No rentals were found for this customer.", 404

        customer_rental_list = []

        for tuple in customer_data:
            video = tuple[1] 
            rental = tuple[2] 

            customer_rental_list.append({
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date
            })
        
        return jsonify(customer_rental_list)
        
# class Video routes
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@videos_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_videos():

    if request.method == "GET":

        videos = Video.query.all()

        video_list = []

        for video in videos:
            video_list.append(video.to_json())

        return jsonify(video_list)

    if request.method == "POST":

        request_body = request.get_json()

        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return {
                "details": "Invalid data.  Missing title, release date, and/or total inventory."
            }, 400
        
        new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"],
                        available_inventory=request_body["total_inventory"]
                        )

        db.session.add(new_video)
        db.session.commit()

        return new_video.to_json(), 201
        

@videos_bp.route("<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_video(video_id):

    video = Video.query.get(video_id)
    
    if video == None:
        return "Video not found.", 404
    
    if request.method == "GET":
        return video.to_json()

    if request.method == "PUT":

        video_data = request.get_json()

        video.title = video_data["title"]
        video.release_date = video_data["release_date"]
        video.total_inventory = video_data["total_inventory"]

        db.session.commit()

        return video.to_json()

    if request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id": video.id,
            "details": f'Video {video.id}: {video.title} successfully deleted.'
        })

# Lists customers for each video
@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def handle_video_rentals(video_id):

        video_data = db.session.query(Customer, Video, CustomerVideoRental).join(Customer, Customer.id==CustomerVideoRental.customer_id)\
            .join(Video, Video.id==CustomerVideoRental.video_id).filter(Video.id == video_id).all()
        
        if video_data is None: 
            return "No customers are renting this video.", 404

        video_rental_list = []

        for tuple in video_data:
            customer = tuple[0] 
            rental = tuple[2] 

            video_rental_list.append({
                "name": customer.name,
                "phone": customer.phone_num,
                "postal_code": customer.postal_code,
                "due_date": rental.due_date
            })
        
        return jsonify(video_rental_list)

# class CustomerVideoRentalroutes
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def handle_rentals_checkout():

    if request.method == "POST":

        rental_data = request.get_json()

        # if type(rental_data["customer_id"]) != int or type(rental_data["video_id"]) != int:
        if not isinstance(rental_data["customer_id"], int) or not isinstance(rental_data["video_id"], int):
            return {
                "details": "Invalid ID data type."
            }, 400

        new_rental = CustomerVideoRental(customer_id=rental_data["customer_id"],
                                        video_id=rental_data["video_id"],
                                        due_date=datetime.datetime.now()+datetime.timedelta(days=7))

        customer = Customer.query.get(new_rental.customer_id)
        video = Video.query.get(new_rental.video_id)

        if customer == None:
            return "Customer not found.", 404

        if video == None:
            return "Video not found.", 404
        elif video.available_inventory <= 0:
            return {
                "details": "0 inventory."
            }, 400

        customer.videos_checked_out_count += 1
        video.available_inventory -= 1

        db.session.add(new_rental)
        db.session.commit()

        return {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
            }


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def handle_rentals_checkin():

    if request.method == "POST":

        checkin_data = request.get_json()

        customer_checkin_id = checkin_data["customer_id"]
        video_checkin_id = checkin_data["video_id"]

        customer = Customer.query.get(customer_checkin_id)
        video = Video.query.get(video_checkin_id)

        if customer == None:
            return "Customer not found.", 404

        if video == None:
            return "Video not found.", 404

        rental = CustomerVideoRental.query.all()
        # rental_test = CustomerVideoRental.query.filter_by(customer_id=customer_checkin_id, video_id=video_checkin_id)
        # rental_test = CustomerVideoRental.query.filter(CustomerVideoRental.customer_id==customer_checkin_id, CustomerVideoRental.video_id==video_checkin_id)
        
        for record in rental:
            if record.customer_id == customer_checkin_id and record.video_id == video_checkin_id and record.outstanding:
                record.outstanding = False

                customer.videos_checked_out_count -= 1
                video.available_inventory += 1

                db.session.commit()

                return {
                "customer_id": customer.id,
                "video_id": video.id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
                }

        else:

            return {
                "details": "Rental not found."
                }, 400

        # match = False

        # for record in rental:
        #     if record.customer_id == customer_checkin_id and record.video_id == video_checkin_id and record.outstanding:
        #         match = True
        #         record.outstanding = False

        # if not match:
        #     return {
        #         "details": "Rental not found."
        #         }, 400

        # customer.videos_checked_out_count -= 1
        # video.available_inventory += 1

        # db.session.commit()

        # return {
        # "customer_id": customer.id,
        # "video_id": video.id,
        # "videos_checked_out_count": customer.videos_checked_out_count,
        # "available_inventory": video.available_inventory
        # }

