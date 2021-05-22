from flask import current_app
from app import db


class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, nullable=True) #nullable=True
    videos_for_rent = db.relationship("Rental", back_populates="videos_rented") 
    # children = relationship("Association", back_populates="parent")
    # In Rentals: 
    # videos_rented = relationship("Video", back_populates="videos_for_rent")

    def videos_to_json_format(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory,
            }


# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
