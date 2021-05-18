from app import db

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    postal_code=db.Column(db.String)
    phone=db.Column(db.String) 
    registered_at=db.Column(db.DateTime, nullable=True, default=None)
    
    #should increase by one, when rental checked out
    videos_checked_out_count=db.Column(db.Integer) 
    
    def video_count(self):
        if self.id == None:
            pass
        else:
            return 0

    def customer_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.video_count()
        }