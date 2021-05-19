from flask import current_app
from app import db
from datetime import datetime # do I need this?

# Establishing many-to-many relationships to between
# Customer and Video Models
# CustomerVideojoin Model/Table
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) ##??
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), \
        primary_key=True) # how about nullable= True or False?
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), \
        primary_key=True)# how about nullable= True or False?, do I add lazy?
    # fake columns
    
    # Customer to Rental is a one to many relationship just like Goal to Task
    rental_date = db.Column(db.DateTime, default=datetime.utcnow(),  
        nullable=False) # maybe

    

    # user = relationship(User, backref=backref("orders", cascade="all, delete-orphan"))
    # product = relationship(Product, backref=backref("orders", cascade="all, delete-orphan"))

# errors, could the errors go here with something like this?
def get_movie(movie_id, customer_id):
    errors = {}
    movie_id_errors = []
    customer_id_errors = []
    if not customer_id:
        customer_id_errors.append('Cant be null')
    if customer_id not in db:
        customer_id_errors.append('Not in db')

    if not movie_id:
        movie_id_errors.append('Cant be null')
    if movie_id not in db:
        movie_id_errors.append('Not in db')

    if movie_id_errors:
        errors['movie_id'] = movie_id_error
    if customer_id_errors:
        errors['customer_id'] = customer_id_errors 
    #...
    if len(errors) > 0:
        print(errors)
        print(movie_id_errors)
        print(customer_id_errors)
        return make_response(errors)# maybe get response can come in 
                                    # routes instead and just return
                                    # errors here
    #
    # {
    #  errors: { "movie_id": ["Can't be null", "Not in db"], 
    #       "customer_id": ["Can't be null", "Not in db"]
    #  }
    # }

# // ...or...

    return {"errors": ["Not Found"]}


def error_response():
    return {"errors": { "Total Inventory": 
                                                [ "can't be blank", 
                                                "is not a number"]}}
# // ...or...

    return {"errors": ["Not Found"]}

#cuerpo de la respuesta una llave por cada error{}

# {"errors": 
#           {"available_inventory": ["can't be blank",
#                                   "is not a number"]}}

# // ...or...

# {
#     "errors": [
#         "Not Found"
#     ]
# }
