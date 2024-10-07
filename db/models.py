from enum import StrEnum, auto

from sqlalchemy.types import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Genre(StrEnum):
    COMEDY = 'комедия'
    ADVENTURE = 'приключения'
    HORROR = 'ужасы'
    ROMANCE = 'мелодрама'
    DETECTIVE = 'детектив'
    SCIENCE_FICTION = 'научная фантастика'
    THRILLER = 'триллер'

    @staticmethod
    def regex() -> str:
        return rf'^({"|".join(Genre)})$'


class UserLevel(StrEnum):
    ELEMENTARY = auto()
    BEGINNER = auto()
    PRE_INTERMEDIATE = 'pre-intermediate'
    INTERMEDIATE = auto()
    ADVANCED = auto()

    @staticmethod
    def regex() -> str:
        return rf'^({"|".join(UserLevel)})$'


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
    published_years: Mapped[str]
    difficulty: Mapped[int]
    n_series: Mapped[int]
    is_ongoing: Mapped[bool]
    description: Mapped[str]
