from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default = 0)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        