from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .model_utilities import date_to_str
from ..db import db

class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    postal_code: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    registered_at: Mapped[str] = mapped_column()
    rentals: Mapped[list["Rental"]] = relationship(back_populates="customer")

    def get_videos_checked_out_count(self):
        count = sum(rental.status == "RENTED" for rental in self.rentals)
        return count

    def has_active_rental(self, video_id):
        try:
            _ = self.get_active_rental_by_video_id(video_id)
        except ValueError:
            return False

        return True
    
    def get_active_rental_by_video_id(self, video_id):
        for rental in self.rentals:
            if rental.video_id == video_id and rental.status == "RENTED":
                return rental
            
        raise ValueError(f"No rental found for video_id {video_id}")

    def get_active_rentals_data(self):
        active_rentals = []
        for rental in self.rentals:
            if rental.status == "RENTED":
                data = {
                    "release_date": rental.video.release_date,
                    "title": rental.video.title,
                    "due_date": rental.due_date,
                }
                active_rentals.append(data)

        return active_rentals

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.get_videos_checked_out_count(),
        }

    def update_customer(self, data):
        self.name = data["name"]
        self.postal_code = data["postal_code"]
        self.phone = data["phone"]

    @classmethod
    def from_dict(cls, data):
        data["registered_at"] = date_to_str(datetime.now())
        Customer.validate_required_fields(data)

        return cls(
            name=data["name"],
            postal_code=data["postal_code"],
            phone=data["phone"],
            registered_at=data["registered_at"]
        )

    @classmethod
    def validate_required_fields(cls, data):
        required_fields = ["name", "postal_code", "phone", "registered_at"]

        for field in required_fields:
            if field not in data or not data[field]:
                raise KeyError(field)