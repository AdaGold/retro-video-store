from sqlalchemy.orm import relationship
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date())
    total_inventory = db.Column(db.Integer)
    customers = relationship("Rental", back_populates="video", passive_deletes=True)

    def as_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "total_inventory": self.total_inventory,
            "available_inventory": self.get_inventory()}

    def get_inventory(self):
        return self.total_inventory - len(self.customers)
