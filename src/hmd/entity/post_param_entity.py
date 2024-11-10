from sqlalchemy import Column, String
from hmd.entity.base_entity import BaseEntity

class PostParamEntity(BaseEntity):
    __tablename__ = "post_param"
    __table_args__ = {'extend_existing': True}
    post_id = Column(String(255), primary_key=True)
    param_key = Column(String(255), primary_key=True)
    param_value = Column(String(1024))