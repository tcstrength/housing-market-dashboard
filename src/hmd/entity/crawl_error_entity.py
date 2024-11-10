from sqlalchemy import Column, Integer, Text
from hmd.entity.base_entity import BaseEntity

class CrawlErrorEntity(BaseEntity):
    __tablename__ = "crawl_error"
    log_id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    html_content = Column(Text)
    crawl_error = Column(Text)