from sqlalchemy import Float, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Baskets(Base):
    __tablename__ = "baskets"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)

    mushrooms: Mapped[list["Mushrooms"]] = relationship("Mushrooms", back_populates="basket")
