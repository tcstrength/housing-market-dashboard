from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class BaseEntity(DeclarativeBase):
    created_at: Mapped[int] = mapped_column(Integer, default=int(datetime.now().timestamp()))
    updated_at: Mapped[int] = mapped_column(Integer, default=int(datetime.now().timestamp()))