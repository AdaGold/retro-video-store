# from app.models import Customer, Video
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import timedelta, datetime

# make a new class inheriting from db.Model (the SQLAlchemy object - SQL like singular class names):
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime, default=((datetime.now() + timedelta(7))), nullable=False)
    # due_date = db.Column(db.DateTime, nullable=False)
    checked_out = db.Column(db.Boolean, default=False, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))  # ForeignKey refers to the Customer Model Primary Key in the table "customers" and column "id"
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))  # ForeignKey refers to the Video Model Primary Key in the table "videos" and column "id"
    
    customer = db.relationship("Customer", backref="rentals", lazy="select") 
    video = db.relationship("Video", backref="rentals", lazy=True) 

    __tablename__= "rentals"

    def to_dict(self):
        print(self.video_id)

        return {
            "due_date": self.due_date, 
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }
    

    @classmethod
    def checkout(cls, customer_id, video_id):

        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)

        new_rental = Rental(
            customer_id = customer.id, 
            video_id = video.id, 
            checked_out = True            # switches the rental checked_out column to True
            )               

        customer.videos_checked_out_count += 1
        video.available_inventory -= 1

        db.session.add(new_rental)
        db.session.commit()

        return new_rental

        
    def checkin(self):

        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }
    

