from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from hmd.entity.base_entity import BaseEntity

class PostDetailEntity(BaseEntity):
    __tablename__ = "post_detail"
    post_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    post_url: Mapped[str] = mapped_column(String(1024))
    post_title: Mapped[str] = mapped_column(String(1024))
    post_type: Mapped[str] = mapped_column(String(16))
    post_desc: Mapped[str] = mapped_column(Text)
    price_in_mil: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    tags: Mapped[str] = mapped_column(String(255))
    posted_at: Mapped[int] = mapped_column(Integer)