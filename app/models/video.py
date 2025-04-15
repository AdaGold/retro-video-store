from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Video(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    release_date: Mapped[str] = mapped_column()
    total_inventory: Mapped[int] = mapped_column()
    rentals: Mapped[list["Rental"]] = relationship(back_populates="video")

    def get_available_inventory(self):
        count = sum(rental.status == "AVAILABLE" for rental in self.rentals)
        return self.total_inventory - count
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.get_available_inventory(),
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title"),
            release_date=data.get("release_date"),
            total_inventory=data.get("total_inventory"),
        )