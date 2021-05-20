# Checks out a video to a customer, and updates the data in the database as such.

# When successful, this request should:

# increase the customer's videos_checked_out_count by one
# decrease the video's available_inventory by one
# create a due date. The rental's due date is the seven days from the current date.
# Required Request Body Parameters
# Request Body Param	Type	Details
# customer_id	integer	ID of the customer attempting to check out this video
# video_id	integer	ID of the video to be checked out

from flask import current_app
from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable = True)



# class FooBarJoin(db.Model):
#     foo_id = db.Column(db.Integer, db.ForeignKey('foo.id'), primary_key=True)
#     bar_id = db.Column(db.Integer, db.ForeignKey('bar.id'), primary_key=True)