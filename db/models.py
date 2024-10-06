from enum import StrEnum

from sqlalchemy.types import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Genre(StrEnum):
    COMEDY = 'комедия'
    ADVENTURE = 'приключения'


class Base(DeclarativeBase):
    ...


class LevelTest(Base):
    __tablename__ = 'level_test'

    id: Mapped[int] = mapped_column(primary_key=True)
    resource_name: Mapped[str]
    resource_link: Mapped[str]
    description: Mapped[str | None]


class Series(Base):
    __tablename__ = 'series'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    en_name: Mapped[str | None]
    genre: Mapped[str]
    start_year: Mapped[int]
    end_year: Mapped[int | None]
    n_series: Mapped[int]
    is_ongoing: Mapped[bool]
    desciption: Mapped[str]
