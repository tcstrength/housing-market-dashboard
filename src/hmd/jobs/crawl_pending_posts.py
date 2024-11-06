from enum import Enum
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from hmd.core import app_config
from hmd.crawlers.list_page import ListPageCrawler
from hmd.entity.base_entity import BaseEntity
from hmd.entity.pending_post_entity import PendingPostEntity

SALES_TEMPLATE="https://www.nhatot.com/mua-ban-bat-dong-san?page={page}"
RENTAL_TEMPLATE="https://www.nhatot.com/thue-bat-dong-san?page={page}"

class ListType(Enum):
    SALES = "sales"
    RENTAL = "rental"

def add_pending_post(engine: Engine, post_id: str, post_url: str, post_type: str):
    with Session(engine) as s:
        exist = (
            s.query(PendingPostEntity)
            .filter(PendingPostEntity.post_id == post_id)
            .count()
        )

        if exist > 0:
            raise RuntimeError(f"Pending post `{post_id}` already exists.")
        
        entity = PendingPostEntity(
            post_id = post_id,
            post_url = post_url,
            post_type = post_type,
            status = "P"
        )
        s.add(entity)
        s.commit()

def crawl_page(engine: Engine, page_no: int, list_type: ListType):
    if page_no <= 0:
        raise ValueError("Argument `page_no` must be greater than 0.")
    if list_type == ListType.SALES:
        template = SALES_TEMPLATE
    elif list_type == ListType.RENTAL:
        template = RENTAL_TEMPLATE
    else:
        raise ValueError("Argument `list_type` not valid.")

    url = template.format(page=page_no)    
    crawler = ListPageCrawler()
    pending_list = crawler.crawl(url)
    logger.info(f"Successfully crawled {len(pending_list)} pending posts.")
    for item in pending_list:
        try:
            add_pending_post(engine, item.post_id, item.post_url, list_type.value)
        except Exception as e:
            logger.warning(e)

if __name__ == "__main__":
    engine = create_engine(app_config.POSTGRES_CONN)
    BaseEntity.metadata.create_all(engine, tables=[PendingPostEntity.__table__])
    crawl_page(engine, 1, ListType.RENTAL)
    crawl_page(engine, 1, ListType.SALES)