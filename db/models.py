# db/models.py
from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.relationships import foreign
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), default="", unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates = "user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token: Mapped[str] = mapped_column(String(255), default="")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    revoked_at: Mapped[datetime | None] = mapped_column(default=None)

    user: Mapped["User"] = relationship("User", back_populates = "refresh_tokens")