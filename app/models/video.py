from app import db

def default_inventory(video):
    return video.get_current_parameters()['total_inventory']
    # why does this work if the function isn't called with ()?

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0, nullable=True)
    available_inventory = db.Column(db.Integer, default=default_inventory, nullable=True)

    def to_json(self): # how to make this work for available_inventory outputs as well?
        """
        Outputs formatted JSON dictionary of video attributes
        """
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
            }

    def from_json(self, input_data):
        """
        Converts JSON input data into new instance of Video
        """
        return self(title=input_data["title"],
        release_date=input_data["release_date"],
        total_inventory=input_data["total_inventory"])
