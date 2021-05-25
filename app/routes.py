from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental




customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp=Blueprint("rentals",__name__, url_prefix="/rentals")



@customer_bp.route("", methods=["POST"])
def valid_customer():
    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    else:
        new_customer = Customer(name=form_data["name"],
                                postal_code=form_data["postal_code"],
                                phone=form_data["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)


@customer_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.cust_dict())
    return make_response(jsonify(customers_response),200)


@customer_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return make_response(customer.cust_dict())


@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    '''update single customer'''
    customer = Customer.query.get_or_404(customer_id) 

    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    db.session.commit()
    return make_response(customer.cust_dict(), 200)

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer= Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response({"id": customer.customer_id}, 200)


@video_bp.route("", methods=["POST"])
def post_video():
    form_data = request.get_json()
    if "title" not in form_data\
        or "release_date" not in form_data\
            or "total_inventory" not in form_data:
        return make_response({"details":"Invalid data"},400)
    else:
        new_video = Video(title = form_data["title"],
                            release_date = form_data["release_date"],
                            total_inventory = form_data["total_inventory"],
                            available_inventory = form_data["total_inventory"])
    
        db.session.add(new_video)
        db.session.commit()
        return make_response({"id": new_video.video_id}, 201)


@video_bp.route("", methods=["GET"])
def get_videos():
    videos= Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.vid_dict())
    return jsonify(video_response),200


@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    return make_response(video.vid_dict())


@video_bp.route("/<video_id>",methods=["PUT"])
def put_video(video_id):

    video = Video.query.get_or_404(video_id)
    form_data = request.get_json()

    if "title" not in form_data\
        or "release_date" not in form_data\
            or "total_inventory" not in form_data:
        return make_response({"details":"invalid data"},400)

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]

    db.session.commit()
    return jsonify(video.vid_dict()), 200


@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):

    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()
    return make_response({"id": video.video_id},200)


@rental_bp.route("/check-out", methods=["POST"])
def checks_out():
    
    form_data = request.get_json()
    customer_id = form_data['customer_id']
    video_id = form_data['video_id']

    if not isinstance(customer_id, int): 
        return make_response({"Customer id":"Invalid"}, 400)
    elif not isinstance(video_id, int):
        return make_response({"Video id":"Invalid data"}, 400)
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None:
        return make_response("Customer does not exist",404)
    if video is None: 
        return make_response("Video does not exist",404)
    if video.available_inventory == 0:
        return make_response(jsonify("There are no available videos"), 400)

    new_rental= Rental(
                    video_id=video_id,
                    customer_id=customer_id)

    customer.videos_checked_out_count +=1
    video.available_inventory -=1
    db.session.add(new_rental)
    db.session.commit()

    return{"customer_id" : customer.customer_id,
            "video_id" : video.video_id,
            "due_date" : new_rental.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory}


@rental_bp.route("/check-in", methods=["POST"])
def checks_in():    
    form_data = request.get_json()
    customer_id = form_data['customer_id']
    video_id = form_data['video_id']

    if not isinstance(customer_id, int): 
        return make_response("Please input a valid customer id", 400)
    if not isinstance(video_id, int):
        return make_response("Please input a valid video id", 400)
        
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None:
        return make_response(jsonify("Customer does not exist:"),404)
    if video is None: 
        return make_response(jsonify("Video does not exist:"),404)

    rental = Rental.query.filter_by(customer_id = customer_id, video_id=video_id).first()
    
    if rental is None:
        return make_response(jsonify("This rental doesn't exist"), 400)
    else:
        customer.videos_checked_out_count -=1
        video.available_inventory +=1

        db.session.delete(rental)
        db.session.commit()

    return make_response({
                        "customer_id": rental.customer_id,
                        "video_id":rental.video_id,
                        "videos_checked_out_count": customer.videos_checked_out_count,
                        "available_inventory": video.available_inventory},200)


@customer_bp.route('/<customer_id>/rentals', methods=["GET"])
def get_cust_rentals(customer_id):

    customer = Customer.query.get(customer_id)   
    if customer is None:
        return make_response("Customer id does not exist", 400)
    
    results= db.session.query(Rental)\
            .join(Customer,Customer.customer_id==Rental.customer_id)\
            .join(Video, Video.video_id==Rental.video_id)\
            .filter(Customer.customer_id==customer_id).all()

    rental_list=[]
    for rental in results:
        rental_list.append({"release_date": Video.query.get(rental.video_id).release_date,
                            "title": Video.query.get(rental.video_id).title,
                            "due_date": rental.due_date})
            
    return make_response(jsonify(rental_list),200)


@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_vid_customers(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"details":"Invalid video id"},404)
        
    results= db.session.query(Rental)\
            .join(Video, Video.video_id==Rental.video_id)\
            .join(Customer, Customer.customer_id==Rental.customer_id)\
            .filter(Video.video_id==video_id).all()

    rental_list = []
    for rental in results:
        rental_list.append(
                    {"due_date": rental.due_date,
                    "name": Customer.query.get(rental.customer_id).name,
                    "phone": Customer.query.get(rental.customer_id).phone,
                    "postal_code": Customer.query.get(rental.customer_id).postal_code})
    
    return make_response(jsonify(rental_list),200)