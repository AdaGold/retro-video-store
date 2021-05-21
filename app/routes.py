from datetime import datetime

from flask import Blueprint, make_response, jsonify, request

from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#Beginning of Wave1
@customer_bp.route('', methods=['GET', 'POST'])
def customers():

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
def customer(id):
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


@video_bp.route('', methods=['GET', 'POST'])
def videos():

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
def video(id):
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
#Ending of Wave1

#Beginning of Wave2

