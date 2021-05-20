# '''
# ========RENTALS ROUTES========
# '''
# ### Checkout a video to a customer and update the database ###
# @rentals_bp.route("/check-out", methods=["POST"])

# def checkout_video():
#     request_body = request.get_json()

#     customer = Customer.query.get(request_body["customer_id"])
#     checked_out_video = Video.query.get(request_body["video_id"])
        
#     # 404: Not Found if missing customer, video, or no available inventory    
#     if "customer_id" not in request_body or "video_id" not in request_body:
#         return jsonify({"details": "Invalid data"}), 404

#     if checked_out_video.available_inventory < 1:
#         return jsonify({"details" : "inventory out of stock"}, 400)         
   
#     # increase the customer's videos_checked_out_count by one
#     customer.videos_checked_out_count += 1
#     # decrease the video's available_inventory by one
#     checked_out_video.available_inventory -= 1

#     new_rental = Rental(
#         customer_id = request_body["customer_id"],
#         video_id = request_body["video_id"],
#         # due_date = datetime.date.today() + timedelta(days=7))
#         due_date = datetime.datetime.now() + datetime.timedelta(days=7))
    
#     db.session.add(new_rental)
#     db.session.commit()

#     rental_result = dict(
#         customer_id = new_rental.customer_id,
#         video_id = new_rental.video_id,
#         due_date = new_rental.due_date,
#         videos_checked_out_count = len(customer.videos_checked_out_count),
#         available_inventory = checked_out_video.available_inventory
#         )

#     return rental_result, 200

# ### Checks in a video to a customer and update the database ###
# @rentals_bp.route("/check-in", methods=["POST"])

# def checkin_video():
#     request_body = request.get_json()

#     customer = Customer.query.get(request_body["customer_id"])
#     checked_in_video = Video.query.get(request_body["video_id"])
        
#     # 404: Not Found if missing customer, video   
#     if "customer_id" not in request_body or "video_id" not in request_body:
#         return jsonify({"details": "Invalid data"}), 404
    
#     # 400: Bad Request if the video and customer do not match a current rental
#     rental = Rental.query.filter_by(
#             customer_id=request_body["customer_id"], 
#             video_id=request_body["video_id"]
#             ).first()
#     print("====Testing====")
#     print(request_body)
#     print(rental)
#     if not rental:
#         return jsonify({"details": "Invalid data"}), 400         
   
#     # decrease the customer's videos_checked_out_count by one
#     customer.videos_checked_out_count -= 1
#     # increase the video's available_inventory by one
#     checked_out_video.available_inventory += 1

#     db.session.delete(rental)
#     db.session.commit()

#     rental_result = dict(
#         customer_id = request_body["customer_id"],
#         video_id = request_body["video_id"],
#         videos_checked_out_count = len(customer.videos_checked_out_count),
#         available_inventory = checked_out_video.available_inventory
#         # available_inventory = checked_out_video.total_inventory - len(checked_out_video.video_rentals)
#         )

#     return rental_result, 200

# ### List the videos a customer currently has checked out ###

# @customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)

# def get_customer_rental(customer_id):
#     # Find the customer with the given id
#     customer = Customer.query.get(customer_id)

#     if customer is None:
#         return make_response("", 404)

#     if customer.videos_checked_out_count == 0:
#         return []

#     return customer.to_dict()

# ### List the customers who currently have the video checked out ###

# @videos_bp.route("/<video_id>/rental", methods=["GET"], strict_slashes=False)

# def list_customers(video_id):
#     # Find the video with the given id
#     video = Video.query.get(video_id)

#     if video is None:
#         return make_response("Video does not exist", 404)
    
#     # when the video is not checked out to any customers
#     if video.total_inventory == available_inventory:
#         return []
    
#         # results = db.session.query(Foo, Bar, FooBarJoin).join(Foo, Foo.id==FooBarJoin.foo_id)\
#         #     .join(Bar, Bar.id==FooBarJoin.bar_id).filter(Foo.id == X).all()

#         # rentals = db.session.query(Rental)\
#         # .join(Video, Video.video_id==Rental.video_id)\
#         # .join(Customer, Customer.customer_id==Rental.customer_id)\
#         # .filter(Video.video_id==video_id).all()

#     return video.to_dict(), 200