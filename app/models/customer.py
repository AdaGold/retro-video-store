from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.get_videos_checked_out_count(),
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            postal_code=data.get("postal_code"),
            phone=data.get("phone"),
            registered_at=data.get("registered_at"),
        )