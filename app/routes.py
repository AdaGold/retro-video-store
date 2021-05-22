from datetime import datetime, timedelta

from flask import Blueprint, make_response, jsonify, request

from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

# Customers

@customer_bp.route('', methods=['GET', 'POST'])
def customer_list():

    if request.method == 'GET': 
        customers = Customer.query.all()
        response = []
        for customer in customers:
            response.append(customer.to_json())
        return jsonify(response), 200

    if request.method == 'POST':
        try:
            request_body = request.get_json()
        except request.BadRequest:
            return "{}", 400

        try:
            customer = Customer(name=request_body['name'],
                                registered_at=datetime.now(),
                                postal_code=request_body['postal_code'],
                                phone=request_body['phone'])
            db.session.add(customer)
            db.session.commit()             
            return jsonify({'id': customer.id}), 201
        except KeyError:
                return "{}", 400



@customer_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customer_detail(id):
    request_body = request.get_json()
    customer = Customer.query.filter_by(id=id).first()
    if not customer:
        return make_response("{}", 404)

    if request.method == 'GET':
        return jsonify(customer.to_json()), 200

    if request.method == 'PUT':
        try:
            customer.name = request_body['name']
            customer.postal_code = request_body['postal_code']
            customer.phone = request_body['phone']
            db.session.commit()
            return customer.to_json(), 200
        except KeyError:
            return make_response("{}", 400)

    if request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return make_response(customer.to_json(), 200)


@customer_bp.route('/<id>/rentals', methods=['GET'])
def customer_rentals(id):
    customer = Customer.query.filter_by(id=id).first()
    response_list = []
    for rental in customer.rentals:
        d = {
            'release_date': rental.video.release_date,
            'title': rental.video.title,
            'due_date': rental.due_date,
        }
        response_list.append(d)
    return jsonify(response_list), 200


# Videos

@video_bp.route('', methods=['GET', 'POST'])
def video_list():

    if request.method == 'GET':
        videos = Video.query.all()
        video_response = []
        for video in videos:
            video_response.append(video.to_json())
        return jsonify(video_response), 200

    if request.method == 'POST':
        request_body = request.get_json()
        try: 
            video = Video(title=request_body['title'],
                        release_date=request_body['release_date'],
                        total_inventory=request_body['total_inventory'])
            db.session.add(video)
            db.session.commit()
            return jsonify({'id': video.id}), 201

        except KeyError:
            return "{}", 400
        

@video_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def video_detail(id):
    request_body = request.get_json()
    video = Video.query.filter_by(id=id).first()
    if not video:
        return make_response('{}', 404)

    if request.method == 'GET':
        return jsonify(video.to_json()),200

    if request.method == 'PUT':
        try:
            video.title = request_body['title'],
            video.release_date = request_body['release_date'],
            video.total_inventory = request_body['total_inventory']
            db.session.commit()
            return video.to_json(), 200
        except KeyError:
            return make_response('{}', 400)

    if request.method == 'DELETE':
        db.session.delete(video)
        db.session.commit()
        return make_response(video.to_json(), 200)



@video_bp.route('/<id>/rentals', methods=['GET'])
def video_rentals(id):
    video = Video.query.filter_by(id=id).first()
    response_list = []
    for rental in video.rentals:
        d = {
            'due_date': rental.due_date,
            'name': rental.customer.name,
            'phone': rental.customer.phone,
            'postal_code': rental.customer.postal_code
        }
        response_list.append(d)
    return jsonify(response_list), 200


# Rentals

@rental_bp.route('/check-out', methods=['POST'])
def rental_checkout():
    request_body = request.get_json()
    video_id = request_body.get('video_id')
    customer_id = request_body.get('customer_id')
    if not type(customer_id) == int or not type(video_id) == int:
        return make_response({'details': 'Invalid data'}, 400)
    video = Video.query.filter_by(id=video_id).first()
    if not video.available_inventory:
        return {'Details': 'No inventory available'}, 400
    
    try:
        rental = Rental(customer_id=request_body['customer_id'],
                        video_id=request_body['video_id'],
                        due_date=str(datetime.today().date() + timedelta(days=7)))
        db.session.add(rental)
        db.session.commit()
        response = {
            'customer_id': rental.customer_id,
            'video_id': rental.video_id,
            'due_date': rental.due_date,
            'videos_checked_out_count': rental.customer.videos_checked_out_count,
            'available_inventory': rental.video.available_inventory,
        }
        return response, 200
    except KeyError:
            return "{}", 400


@rental_bp.route('/check-in', methods=['POST'])
def rental_checkin():
    request_body = request.get_json()
    video_id = request_body.get('video_id')
    customer_id = request_body.get('customer_id')
    if not type(customer_id) == int or not type(video_id) == int:
        return make_response({'details': 'Invalid data'}, 400)
    try:
        video = Video.query.filter_by(id=video_id).first()
        customer = Customer.query.filter_by(id=customer_id).first()
        rental_queryset = Rental.query.filter_by(video_id=video_id, customer_id=customer_id)
        if not rental_queryset.count():
            return {'Details': 'Nope!'}, 400
        rental_queryset.delete()
        db.session.commit()
        response = {
            'customer_id': customer.id,
            'video_id': video.id,
            'videos_checked_out_count': customer.videos_checked_out_count,
            'available_inventory': video.available_inventory,
        }
        return response, 200
    except KeyError:
            return "{}", 400




