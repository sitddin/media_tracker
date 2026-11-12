from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import UniqueConstraint

class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "tmdb_id",
        name="uq_movies_user_tmdb"
    ),
)

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    tmdb_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    user: Mapped["User | None"] = relationship(
    "User",
    back_populates="movies"
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    hashed_password:  Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    movies: Mapped[list["Movie"]] = relationship(
    "Movie",
    back_populates="user"
)