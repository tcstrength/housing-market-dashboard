from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from hmd.entity.base_entity import BaseEntity

class CrawlErrorEntity(BaseEntity):
    __tablename__ = "crawl_error"
    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[str] = mapped_column(Integer)
    html_content: Mapped[str] = mapped_column(Text)
    crawl_error: Mapped[str] = mapped_column(Text)