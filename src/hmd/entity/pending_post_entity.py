from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from hmd.entity.base_entity import BaseEntity

class PendingPostEntity(BaseEntity):
    __tablename__ = "pending_post_entity"
    post_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    post_url: Mapped[str] = mapped_column(String(1024))
    post_type: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(1))