from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = "video"
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer)
    
    customer = relationship("rental", back_populates="video")

    def to_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            }