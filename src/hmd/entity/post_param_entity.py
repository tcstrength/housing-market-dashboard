from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from hmd.entity.base_entity import BaseEntity

class PostParamEntity(BaseEntity):
    __tablename__ = "post_param"
    post_id: Mapped[int] = mapped_column(String(255), primary_key=True)
    param_key: Mapped[str] = mapped_column(String(255), primary_key=True)
    param_value: Mapped[str] = mapped_column(String(1024))