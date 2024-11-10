from sqlalchemy import Column, Integer, String, Text
from hmd.entity.base_entity import BaseEntity

class PostDetailEntity(BaseEntity):
    __tablename__ = "post_detail"
    __table_args__ = {'extend_existing': True}
    post_id = Column(Integer, primary_key=True, autoincrement=False)
    post_url = Column(String(1024))
    post_title = Column(String(1024))
    post_type = Column(String(16))
    post_desc = Column(Text)
    price_in_mil = Column(Integer)
    address = Column(String(255))
    tags = Column(String(255))
    posted_at = Column(Integer)