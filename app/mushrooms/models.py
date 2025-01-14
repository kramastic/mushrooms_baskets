from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Mushrooms(Base):
    __tablename__ = "mushrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    eatable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    freshness: Mapped[int] = mapped_column(Integer, nullable=False) #в днях

    basket_id: Mapped[int|None] = mapped_column(ForeignKey("baskets.id"),  nullable=True)
    basket: Mapped["Baskets"] = relationship("Baskets", back_populates="mushrooms")

