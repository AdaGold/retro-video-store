from app import db
from app.models import video
from app.models import customer
from app.models.customer import Customer
from app.models.rentals import Rental
from app.models.video import Video
from flask import json, request, Blueprint, make_response, jsonify, Flask
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
import os
from dotenv import load_dotenv
import requests

load_dotenv()

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# CRUD CUSTOMERS
@customer_bp.route("", methods=["GET"])
def list_customers():
    """Retrieves all customers and their related data from database"""
    customers = Customer.query.all()
    print('customers: ', type(customers)) # list of customer objects

    list_of_customers = []
    if not customers:
        return jsonify(list_of_customers)
    for customer in customers: # for every Customer instance/object in the list of them
        print('WHAT D.TYPE IS CUSTOMER? ', type(customer))
        list_of_customers.append(customer.to_json())
        print('list of customers: ', list_of_customers) # list of dicts
    return jsonify(list_of_customers) # jsonified list of dicts;;;;; LJ -- double formatting???

@customer_bp.route("/<customer_id>", methods=["GET"])
def list_single_customer(customer_id):
    """Retrieves data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    #print('SINGLE CUSTOMER: ', single_customer)
    if not single_customer:
        return make_response({"details": f"There is no customer in the database with ID #{customer_id}"}, 404)

    #print('before: ', type(single_customer.postal_code))
    single_customer.postal_code = int(single_customer.postal_code)
    #print('after: ', type(single_customer.postal_code))

    return jsonify(single_customer.to_json())

@customer_bp.route("", methods=["POST"])
def create_customer():
    """Create a customer for the database"""
    request_body = request.get_json() # form data submitted by user; telling flask tht it expects http request to this endpoint to contain txt that's structured as json; read that txt and give to me in json format
    
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: # checks key; this way only prevents if the key is missing from the user's info (lets you click continue even if you gave an empty str as your phone number)
        return make_response({"details": "Customer name, phone number and postal code must all be provided, and they must be strings"}, 400)
    
    # TAKE OFF REGISTER_AT LINE AND VIDEOS_CHECKED...LINE TO PASS TESTS...
    new_customer = Customer(name=request_body["name"],
    postal_code=request_body["postal_code"],
    phone_number=request_body["phone"],
    register_at=datetime.now()) #, # changing bc the customer is registered when theyre created; line used to be ' register_at=request_body["registered_at"], '
    #videos_checked_out_count=request_body["videos_checked_out_count"]) ## add all attr.s you want user to be able to add when creating their customer acct

    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    """Updates data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)
    
    request_body = request.get_json()
    # check for missing keys and that each value type is the appropriate data type (str)
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: 
        return make_response({"details": "Customer name, phone number and postal code must all be provided."}, 400)
    elif (type(request_body["name"]) != str) or (type(request_body["postal_code"]) != int) or (type(request_body["phone"]) != str):
        return make_response({"details: Customer name and phone number must be strings. Postal code must be an integer."}, 400)
    #intified_postal_code = int(request_body["postal_code"])
    single_customer.name = request_body["name"]
    single_customer.postal_code = request_body["postal_code"] # intified_postal_code  THIS IS NOT READING AS AN INT EVEN THOUGH IT SHOULD...
    single_customer.phone_number = request_body["phone"]
    # commented out following only to pass tests...
    #single_customer.videos_checked_out_count = request_body["videos_checked_out_count"] # no line for register_at attr bc registration happens when customer's created

    db.session.commit()
    return jsonify(single_customer.to_json())

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    """Delete a specific customer from the database"""
    single_customer = Customer.query.get(customer_id)
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)

    db.session.delete(single_customer)
    db.session.commit()
    return make_response({"id": single_customer.customer_id}, 200)

# CRUD VIDEOS
@video_bp.route("", methods=["GET"])
def list_videos():
    """Retrieves all videos and their related data from database"""
    videos = Video.query.all()
    list_of_videos = []
    
    if not videos:
        return jsonify(list_of_videos)
    
    for video in videos:
        list_of_videos.append(video.to_json())
    return jsonify(list_of_videos)

@video_bp.route("/<video_id>", methods=["GET"])
def list_single_video(video_id):
    """Retrieves data of specific video"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"There is no video in the database with ID #{video_id}"}, 404)
    return jsonify(single_video.to_json())

@video_bp.route("", methods=["POST"])
def create_video():
    """Create a video for the database"""
    request_body = request.get_json() # form data submitted by user

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: # checks key; this way only prevents if the key is missing from the user's info (lets you click continue even if you gave an empty str as your phone number)
        return make_response({"details": "Video title, release date and total in inventory must all be provided, and they must be string, datetime and integer values, respectively."}, 400)

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"], # offer this format when creating a video: "1981-08-12" and it'll turn it to datetime obj in response
                    total_inventory=request_body["total_inventory"], #,   # set this to 0??? to address 'null should be 0' in postman test? 
                    # commented next line out for tests
                    available_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()
    return make_response({"id": new_video.video_id}, 201)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_single_video(video_id):
    """Updates data of a specific video"""
    single_video = Video.query.get(video_id)
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    request_body = request.get_json()
    # check for missing values and that each value type is the appropriate data type
    print(request_body) # {'title': 'The Matrix 5', 'release_date': '2021-08-12', 'total_inventory': 1, 'available_inventory': 0}
    print(type(request_body["release_date"])) # str

    ## CONVERT STR TO DATETIME HERE, THEN PROCESS IT IN THE FOLLOWING LINE
    request_body["release_date"] = datetime.fromisoformat(request_body["release_date"])
    print('TYPE: ', type(request_body["release_date"])) # checks that str is turned into datetime obj successfully
    

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: # or "available_inventory" not in request_body:
        return make_response({"details": "Video title, release date and inventory counts must all be provided."}, 400)
    elif (type(request_body["title"]) != str) or (type(request_body["release_date"]) != datetime) or (type(request_body["total_inventory"]) != int): # or (type(request_body["available_inventory"]) != int):
        return make_response({"details": "Video title must be a string, release date must be a datetime object and inventory/available counts must both be integers."}, 400)
    else:
        single_video.title = request_body["title"]
        single_video.release_date = request_body["release_date"]
        single_video.total_inventory = request_body["total_inventory"]
        #single_video.available_inventory = request_body["available_inventory"]

        db.session.commit()
        return jsonify(single_video.to_json())

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    """Delete a specific video from the database"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    db.session.delete(single_video)
    db.session.commit()
    return make_response({"id": single_video.video_id}, 200) 

# CRUD RENTALS
@rental_bp.route("/check-out", methods=["POST"])
def check_out_video():
    """Check out a video to a customer"""
    request_body = request.get_json() # {'customer_id': 7, 'video_id': 'not a valid id', 'check_out_date': datetime.datetime(2021, 5, 20, 18, 11, 13, 797662)}

    if "customer_id" not in request_body or "video_id" not in request_body: # only check that keys exist in arg being passed by API
        return make_response({"details": "Incomplete entry. Please include customer ID and video ID."}, 400)
    elif (type(request_body["customer_id"]) != int) or (type(request_body["video_id"]) != int):
        return make_response({"details": "Customer ID and video ID must be integers!"}, 400)
    loaned_video = Rental(customer_id=request_body["customer_id"],
                                video_id=request_body["video_id"],
                                check_out_date=datetime.now()) 

    customer = Customer.query.get(loaned_video.customer_id)
    video = Video.query.get(loaned_video.video_id)

    if customer is None or video is None: # 'is' or '=='?
        return make_response({"details": "The customer and/or the video does not exist."}, 404)
    if video.available_inventory == 0:
        return make_response({"details": "All copies of this video are checked out."}, 400)

    customer.videos_checked_out_count += 1 # add 1 to the customer's num vids checked out
    video.available_inventory -= 1 # remove 1 from total available inventory bc someone has it now

    db.session.add(loaned_video)
    db.session.commit()
    return jsonify(loaned_video.to_json())

@rental_bp.route("/check-in", methods=["POST"])
def check_in_video():
    """Checks a customer's video back in"""
    request_body = request.get_json() # {"customer_id": 16, "video_id": 17}
    #print('CHECK IN RB: ', request_body)

    for detail in ["customer_id", "video_id"]: 
        if not (detail in request_body):
            return make_response({}, 400) # checks that incoming request body is complete (keys all present)

    returned_video = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"])
    customer = Customer.query.get(returned_video.customer_id)
    video = Video.query.get(returned_video.video_id)

    if customer is None or video is None: # 'is' or '=='?
        return make_response({"details": "The customer and/or the video does not exist."}, 404)
    if (video.video_id != request_body["video_id"]) or (customer.customer_id != request_body["customer_id"]):
        return make_response("", 400)
    if video.available_inventory == video.total_inventory:
        return make_response({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count, 
            "available_inventory": video.available_inventory
            }, 400)

    customer.videos_checked_out_count -= 1 # add 1 to the customer's num vids checked out
    video.available_inventory += 1 # remove 1 from total available inventory bc someone has it now

    db.session.add(returned_video)
    db.session.commit()
    return jsonify({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count, 
            "available_inventory": video.available_inventory
            })

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def list_customer_videos(customer_id):
    """Retrieves all videos a customer has checked out"""
    hold_whats_relevant = {} # for final return 
    hold_dictified_entities = [] # hold obj>dict entities in here
    customer_entity = [] # hold separated obj in prep for dict rebuild
    dictified_ce = {} # store rebuilt dict
    video_entity = [] # hold separated obj in prep for dict rebuild
    dictified_ve = {} # store rebuilt dict
    rental_entity = [] # hold separated obj in prep for dict rebuild
    dictified_re = {} # store rebuilt dict

    # get all videos associated with a customer at ID X:
    # result will be an array of tuples.  Each tuple will hold a Customer instance, a Video instance 
    # and a Rental instance (in the order they are listed in the query):
    customer_vids = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id==customer_id).all()
    
    # customer_vids = [
    #   ({
            #"id": self.customer_id,  
            #"name": self.name,
            #"phone": self.phone_number,
            #"postal_code": self.postal_code,
            #"registered_at": check_registration,
            #"videos_checked_out_count": self.videos_checked_out_count}),
            # 
            # ({
            #"id": self.video_id,
            #"title": self.title,
            #"release_date": self.release_date,
            #"total_inventory": self.total_inventory,
            #"available_inventory": self.available_inventory}), 
            # 
            # ({
            #"customer_id": self.customer_id,
            #"video_id": self.video_id,
            #"due_date": self.check_out_date + (timedelta(days=7)),
            #"videos_checked_out_count": self.renter.videos_checked_out_count,
            #"available_inventory": self.video.available_inventory})
            # 
            # ]

    # extract entities from list of tuples
    for tupled_entity in customer_vids: # for every tupled entity instance in the list, ({"":"", "":""})
        if tupled_entity[0] == None: # if first entity is not a customer, it means the customer doenst exist..
            return make_response({"details": "Customer does not exist"}, 404)
        for entity in tupled_entity: # for every instance-itself in the tuple, {"":"", "":""},  # entity = <Customer 24>
            if type(entity) == Customer: # put all the customer info together in same dict
                if entity.videos_checked_out_count == 0:
                    return jsonify([])
                customer_entity.append(entity) # customer_entity = [<Customer 9>]
                dictified_ce["id"] = entity.customer_id # build the dict
                dictified_ce["name"] = entity.name
                dictified_ce["phone"] = entity.phone_number
                dictified_ce["postal_code"] = entity.postal_code
                dictified_ce["registered_at"] = entity.register_at
                dictified_ce["videos_checked_out_count"] = entity.videos_checked_out_count
                hold_dictified_entities.append(dictified_ce) # add built dict to final workable list; now [ 1 ] dict inside
            elif type(entity) == Video:
                video_entity.append(entity) # video_entity = [<Video 9>]
                dictified_ve["id"] = entity.video_id # build the dict
                dictified_ve["title"] = entity.title
                dictified_ve["release_date"] = entity.release_date
                dictified_ve["total_inventory"] = entity.total_inventory
                dictified_ve["available_inventory"] = entity.available_inventory
                hold_dictified_entities.append(dictified_ve) # add built dict to final workable list; now [ 2 ] dicts inside
            elif type(entity) == Rental:
                rental_entity.append(entity) # rental_entity = [<Rental 15>]
                dictified_re["customer_id"] = entity.customer_id # build the dict
                dictified_re["video_id"] = entity.video_id
                dictified_re["due_date"] = entity.check_out_date + (timedelta(days=7))
                dictified_re["videos_checked_out_count"] = entity.renter.videos_checked_out_count
                dictified_re["available_inventory"] = entity.video.available_inventory
                hold_dictified_entities.append(dictified_re) # add built dict to workable list; now [ 3 ] dicts inside

    # hold_dictified_entities = [
    #   {'id': 12, 'name': 'Lars Sankar', 'phone': '111-111-1111', 'postal_code': 75007, 'registered_at': datetime.datetime(2021, 5, 21, 14, 47, 34, 892201), 'videos_checked_out_count': 1}, 
    #   {'id': 12, 'title': 'Blacksmith Of The Banished', 'release_date': datetime.datetime(1979, 1, 18, 0, 0), 'total_inventory': 1, 'available_inventory': 0}, 
    #   {'customer_id': 12, 'video_id': 12, 'due_date': datetime.datetime(2021, 5, 28, 14, 47, 35, 37057), 'videos_checked_out_count': 1, 'available_inventory': 0}
    # ]

    for dictified_entity in hold_dictified_entities: # for every dict in the list
        if "release_date" in dictified_entity: # if 'release_date' key is in that dictified entity, recreate it and its info in the final dict for return
            hold_whats_relevant["release_date"] = dictified_entity["release_date"]
            print("RELEASE DATE: ", hold_whats_relevant["release_date"])
        if "title" in dictified_entity: # if 'title' is in that entity, recreate it and its info in the final dict for return
            hold_whats_relevant["title"] = dictified_entity["title"]
            print("TITLE: ", hold_whats_relevant["title"])
        if "due_date" in dictified_entity: # if 'due_date' is in that entity, recreate it and its info in the final dict for return
            dictified_entity["due_date"] = str(dictified_entity["due_date"])
            hold_whats_relevant["due_date"] = dictified_entity["due_date"]
            print("DUE DATE: ", hold_whats_relevant["due_date"])
    print('FINAL FOR COMPARE: ', hold_whats_relevant) 
    # hold_whats_relevant = {'release_date': datetime.datetime(1979, 1, 18, 0, 0), 
    #                        'title': 'Blacksmith Of The Banished', 
    #                         'due_date': datetime.datetime(2021, 5, 28, 15, 8, 26, 463780)
    #                       }
    return jsonify(hold_whats_relevant) # wrap above in list: [{..hold_whats_relevant...}]
    
# jsonify and return finished product
# which should look like this: 
# [
#     {
#         "release_date": "Wed, 01 Jan 1958 00:00:00 GMT",
#         "title": "Vertigo",
#         "due_date": "Thu, 13 May 2021 19:27:47 GMT",
#     },
#     {
#         "release_date": "Wed, 01 Jan 1941 00:00:00 GMT",
#         "title": "Citizen Kane",
#         "due_date": "Thu, 13 May 2021 19:28:00 GMT",
#     }
# ]

# >>> check!

# `GET /videos/<id>/rentals`
@video_bp.route("/<video_id>/rentals", methods=["GET"])
def list_video_renters(video_id):
    """List the customers who currently have the video checked out"""
    hold_whats_relevant = {} # for final return 
    hold_dictified_entities = [] # hold obj>dict entities in here
    customer_entity = [] # hold separated obj in prep for dict rebuild
    dictified_ce = {} # store rebuilt dict
    video_entity = [] # hold separated obj in prep for dict rebuild
    dictified_ve = {} # store rebuilt dict
    rental_entity = [] # hold separated obj in prep for dict rebuild
    dictified_re = {} # store rebuilt dict

    # get all customers associated with a video at ID X:
    # result will be an array of tuples.  Each holding a Video instance, Customer instance
    # and a Rental instance (in the order they are listed in the query):
    videos_by_customer = db.session.query(Video, Customer, Rental).join(Video, Video.video_id==Rental.video_id)\
        .join(Customer, Customer.customer_id==Rental.customer_id).filter(Video.video_id==video_id).all()
    
    # videos_by_customer = [
    #   # ({
            #"id": self.video_id,
            #"title": self.title,
            #"release_date": self.release_date,
            #"total_inventory": self.total_inventory,
            #"available_inventory": self.available_inventory}),
            # 
            # ({
            #"id": self.customer_id,  
            #"name": self.name,
            #"phone": self.phone_number,
            #"postal_code": self.postal_code,
            #"registered_at": check_registration,
            #"videos_checked_out_count": self.videos_checked_out_count}),
            # 
            # 
            # ({
            #"customer_id": self.customer_id,
            #"video_id": self.video_id,
            #"due_date": self.check_out_date + (timedelta(days=7)),
            #"videos_checked_out_count": self.renter.videos_checked_out_count,
            #"available_inventory": self.video.available_inventory})
            # 
            # ]

    # extract entities from list of tuples
    for tupled_entity in videos_by_customer: # for every tupled entity instance in the list, ({"":"", "":""})
        if tupled_entity[0] == None: # if first entity is not a video, it means the video doenst exist..
            return make_response({"details": "Video does not exist"}, 404)
        for entity in tupled_entity: # for every instance-itself in the tuple, {"":"", "":""},  # entity = <Video 24>
            if type(entity) == Video:
                if entity.total_inventory == entity.available_inventory:
                    return jsonify([])
                video_entity.append(entity) # video_entity = [<Video 9>]
                dictified_ve["id"] = entity.video_id # build the dict
                dictified_ve["title"] = entity.title
                dictified_ve["release_date"] = entity.release_date
                dictified_ve["total_inventory"] = entity.total_inventory
                dictified_ve["available_inventory"] = entity.available_inventory
                hold_dictified_entities.append(dictified_ve) # add built dict to final workable list; now [ 1 ] dict inside
            elif type(entity) == Customer: # put all the customer info together in same dict
                customer_entity.append(entity) # customer_entity = [<Customer 9>]
                dictified_ce["id"] = entity.customer_id # build the dict
                dictified_ce["name"] = entity.name
                dictified_ce["phone"] = entity.phone_number
                dictified_ce["postal_code"] = entity.postal_code
                dictified_ce["registered_at"] = entity.register_at
                dictified_ce["videos_checked_out_count"] = entity.videos_checked_out_count
                hold_dictified_entities.append(dictified_ce) # add built dict to final workable list; now [ 2 ] dicts inside
            elif type(entity) == Rental:
                rental_entity.append(entity) # rental_entity = [<Rental 15>]
                dictified_re["customer_id"] = entity.customer_id # build the dict
                dictified_re["video_id"] = entity.video_id
                dictified_re["due_date"] = entity.check_out_date + (timedelta(days=7))
                dictified_re["videos_checked_out_count"] = entity.renter.videos_checked_out_count
                dictified_re["available_inventory"] = entity.video.available_inventory
                hold_dictified_entities.append(dictified_re) # add built dict to workable list; now [ 3 ] dicts inside
    print("HOWDY: ", hold_dictified_entities)
    # hold_dictified_entities = [
    #   {'id': 12, 'name': 'Lars Sankar', 'phone': '111-111-1111', 'postal_code': 75007, 'registered_at': datetime.datetime(2021, 5, 21, 14, 47, 34, 892201), 'videos_checked_out_count': 1}, 
    #   {'id': 12, 'title': 'Blacksmith Of The Banished', 'release_date': datetime.datetime(1979, 1, 18, 0, 0), 'total_inventory': 1, 'available_inventory': 0}, 
    #   {'customer_id': 12, 'video_id': 12, 'due_date': datetime.datetime(2021, 5, 28, 14, 47, 35, 37057), 'videos_checked_out_count': 1, 'available_inventory': 0}
    # ]

    for dictified_entity in hold_dictified_entities: # for every dict in the list
        if "name" in dictified_entity: # if 'name' key is in that dictified entity, recreate it and its info in the final dict for return
            hold_whats_relevant["name"] = dictified_entity["name"]
            print("NAME: ", hold_whats_relevant["name"])
        elif "postal_code" in dictified_entity: # if 'postal_code' key is in that dictified entity, recreate it and its info in the final dict for return
            hold_whats_relevant["postal_code"] = dictified_entity["postal_code"]
            print("POSTAL_CODE: ", hold_whats_relevant["postal_code"])
        elif "phone" in dictified_entity: # if 'phone' is in that entity, recreate it and its info in the final dict for return
            hold_whats_relevant["phone"] = dictified_entity["phone"]
            print("PHONE: ", hold_whats_relevant["phone"])
        elif "due_date" in dictified_entity: # if 'due_date' is in that entity, recreate it and its info in the final dict for return
            dictified_entity["due_date"] = str(dictified_entity["due_date"])
            hold_whats_relevant["due_date"] = dictified_entity["due_date"]
            print("DUE DATE: ", hold_whats_relevant["due_date"])
    print('FINAL FOR COMPARE: ', hold_whats_relevant) 
    # hold_whats_relevant = {'release_date': datetime.datetime(1979, 1, 18, 0, 0), 
    #                        'title': 'Blacksmith Of The Banished', 
    #                         'due_date': datetime.datetime(2021, 5, 28, 15, 8, 26, 463780)
    #                       }
    return jsonify(hold_whats_relevant) # wrap above in list: [{..hold_whats_relevant...}]


