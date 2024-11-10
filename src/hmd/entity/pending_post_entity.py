from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column, Integer, String
from hmd.entity.base_entity import BaseEntity

class PendingPostEntity(BaseEntity):
    __tablename__ = "pending_post_entity"
    __table_args__ = {'extend_existing': True}
    post_id = Column(Integer, primary_key=True, autoincrement=False)
    post_url = Column(String(1024))
    post_type = Column(String(16))
    status = Column(String(1))