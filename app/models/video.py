from app import db

def avail_inv_default(context):
    return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=avail_inv_default)
    release_date = db.Column(db.DateTime)
    rentals = db.relationship("Rental", back_populates="video", lazy=True)

    def video_to_json(self):
        to_json = {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory,
            "release_date": self.release_date,
        }
        return to_json