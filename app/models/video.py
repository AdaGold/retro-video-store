from app import db

# make a new class inheriting from db.Model (the SQLAlchemy object - SQL like singular class names):
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, nullable=False)

    # One to many relationship: one video has been rented many times
    videos = db.relationship("Rental", backref="videos", lazy=True)  

    __tablename__= "videos"

    def to_dict(self):

        make_dict = {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
       
        return make_dict