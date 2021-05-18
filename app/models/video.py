from app import db

class Video(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String)
    release_date=db.Column(db.String)
    total_inventory=db.Column(db.Integer) #required
    
    #decrease by one with rentals/checkout
    available_inventory=db.Column(db.Integer)

    # def av_inventory(self):
    #     if 

    def video_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.total_inventory-1
        }