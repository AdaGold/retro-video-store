from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Rental(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    due_date: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default="RENTED")
    customer: Mapped["Customer"] = relationship(back_populates="rentals")
    video: Mapped["Video"] = relationship(back_populates="rentals")

    def to_dict(self):
        videos_checked_out_count = self.customer.get_videos_checked_out_count()
        available_inventory = self.video.get_available_inventory()

        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }
    
    @classmethod
    def validate_required_fields(self, data):
        required_fields = ["customer_id", "video_id", "due_date"]

        for field in required_fields:
            if field not in data or not data[field]:
                raise KeyError(field)

    @classmethod
    def from_dict(cls, data):
        Rental.validate_required_fields(data)

        return cls(
            customer_id=data["customer_id"],
            video_id=data["video_id"],
            due_date=data["due_date"],
        )