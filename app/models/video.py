from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Video(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    release_date: Mapped[str] = mapped_column()
    total_inventory: Mapped[int] = mapped_column()
    rentals: Mapped[list["Rental"]] = relationship(back_populates="video")

    def get_available_inventory(self):
        count = sum(rental.status == "RENTED" for rental in self.rentals)
        return self.total_inventory - count
    
    def is_available(self):
        return self.get_available_inventory() > 0

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.get_available_inventory(),
        }
    
    def update_video(self, data):
        self.title = data["title"]
        self.release_date = data["release_date"]
        self.total_inventory = data["total_inventory"]

    @classmethod
    def from_dict(cls, data):
        Video.validate_required_fields(data)

        return cls(
            title=data.get("title"),
            release_date=data.get("release_date"),
            total_inventory=data.get("total_inventory"),
        )

    @classmethod
    def validate_required_fields(cls, data):
        required_fields = ["title", "release_date", "total_inventory"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise KeyError(field)