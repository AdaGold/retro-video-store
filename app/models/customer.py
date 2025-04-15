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
    
    def update_customer(self, data):
        self.name = data["name"]
        self.postal_code = data["postal_code"]
        self.phone = data["phone"]
    
    @classmethod
    def validate_required_fields(self, data):
        required_fields = ["name", "postal_code", "phone", "registered_at"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise KeyError(field)

    @classmethod
    def from_dict(cls, data):
        Customer.validate_required_fields(data)
        print(data)

        return cls(
            name=data["name"],
            postal_code=data["postal_code"],
            phone=data["phone"],
            registered_at=data["registered_at"]
        )