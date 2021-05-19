import re
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    available_inventory = db.Column(db.String, nullable=True)

    @classmethod
    def create(cls, title, release_date, total_inventory):
        new_video = Video(title=title, release_date=release_date, total_inventory=total_inventory)
        db.session.add(new_video)
        db.session.commit()
        return new_video

    @classmethod
    def read_all(cls):
        videos = Video.query.all()
        return videos
        
    @classmethod
    def read(cls, video_id):
        video = Video.query.get(video_id)
        return video

    @classmethod
    def update(cls, video_id, title=None, release_date=None, total_inventory=None):
        video = Video.read(video_id)
        if title:
            video.title = title
        if release_date:
            video.release_date = release_date
        if total_inventory:
            video.total_inventory = total_inventory
        db.session.commit()
        return video

    @classmethod
    def delete(cls, video_id):
        video = Video.read(video_id)
        db.session.delete(video)
        db.session.commit()

    def to_dict(self):
        format_string = '%Y-%m-%d' # 1979-01-18
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date.strftime(format_string),
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }