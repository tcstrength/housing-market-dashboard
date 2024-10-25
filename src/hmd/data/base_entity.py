from sqlalchemy import func as F
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class BaseEntity(DeclarativeBase):
    created_at: Mapped[int] = mapped_column(Integer, F.extract("epoch", F.current_timestamp()))
    updated_at: Mapped[int] = mapped_column(Integer, F.extract("epoch", F.current_timestamp()))