from sqlalchemy import String
from sqlalchemy import Integer
from hmd.data.base_entity import *

class PostEntity(BaseEntity):
    __tablename__ = "post_entity"
    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ext_id: Mapped[str] = mapped_column(String(16))
    post_title: Mapped[str] = mapped_column(String(255))
    post_desc: Mapped[str] = mapped_column(String(-1))
    address: Mapped[str] = mapped_column(String(255))
    last_update: Mapped[str] = mapped_column(String(255))