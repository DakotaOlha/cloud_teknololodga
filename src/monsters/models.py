from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models import User
from src.core.database import Base, TimestampMixin


class Monster(Base, TimestampMixin):
    __tablename__ = "monsters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    monster_type: Mapped[str] = mapped_column(String(100), nullable=False)
    challenge_rating: Mapped[float] = mapped_column(Float, nullable=False)
    hit_points: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", backref="monsters")

    def __repr__(self):
        return f"<Monster(id={self.id}, name={self.name}, type={self.monster_type})>"
