from app import db 

def mydefault(context):
    return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, nullable=True)
    available_inventory = db.Column(db.Integer, default=mydefault)

    def to_json(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }