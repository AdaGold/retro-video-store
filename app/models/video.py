from app import db
from app.models.rental import Rental

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    rentals = db.relationship('Rental', backref = 'video', lazy = True)
    #customers = db.relationship("Customer", secondary="rental", back_populates="videos")

    def to_video_object(self):
        return {
        "id": self.id,
        "title": self.title,
        "release_date": self.release_date,
        "total_inventory": self.total_inventory
    }

    def videos_rental_query(self):
        rental_query = Rental.query.filter_by(video_id = self.id)
        return rental_query.count()
    
    def check_out_available_inventory(self):
        return self.total_inventory - self.videos_rental_query()

    def check_in_available_inventory(self):
        return self.total_inventory + self.videos_rental_query()