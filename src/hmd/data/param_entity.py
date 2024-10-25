from sqlalchemy import String
from sqlalchemy import Integer
from hmd.data.base_entity import *

class ParamEntity(BaseEntity):
    __tablename__ = "post_entity"
    post_id: Mapped[int] = mapped_column(Integer)
    param_key: Mapped[str] = mapped_column(String(255))
    param_value: Mapped[str] = mapped_column(String(255))