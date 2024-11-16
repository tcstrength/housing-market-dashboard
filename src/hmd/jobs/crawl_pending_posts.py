from enum import Enum
from loguru import logger
from multiprocessing.pool import ThreadPool
from sqlalchemy import create_engine
from hmd.core import app_config
from hmd.crawlers.base_crawler import CrawlMethod
from hmd.crawlers.list_page import ListPageCrawler
from hmd.entity.base_entity import BaseEntity
from hmd.entity.pending_post_entity import PendingPostEntity
from sqlalchemy.orm import sessionmaker
from psycopg2.errors import UniqueViolation

SALES_TEMPLATE="https://www.nhatot.com/mua-ban-bat-dong-san?page={page}"
RENTAL_TEMPLATE="https://www.nhatot.com/thue-bat-dong-san?page={page}"

class ListType(Enum):
    SALES = "sales"
    RENTAL = "rental"

def add_pending_post(engine, post_id: str, post_url: str, post_type: str):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    result = post_id
    try:
        # Perform database operations here
        exist = (
            session.query(PendingPostEntity)
            .filter(PendingPostEntity.post_id == post_id)
            .count()
        )

        if exist > 0:
            raise UniqueViolation()
        
        entity = PendingPostEntity(
            post_id = post_id,
            post_url = post_url,
            post_type = post_type,
            status = "P"
        )
        session.add(entity)
        session.commit()
    except UniqueViolation as e:
        result = "-2"
        logger.warning(f"Pending post `{post_id}` already exists.")
    except Exception as e:
        logger.warning(e)
        result = "-1"
    finally:
        # Close the session
        session.close()
    return result

def crawl_page(page_no: int, list_type: ListType, crawl_method: CrawlMethod):
    engine = create_engine(app_config.POSTGRES_CONN)
    if page_no <= 0:
        raise ValueError("Argument `page_no` must be greater than 0.")
    if list_type == ListType.SALES:
        template = SALES_TEMPLATE
    elif list_type == ListType.RENTAL:
        template = RENTAL_TEMPLATE
    else:
        raise ValueError("Argument `list_type` not valid.")

    url = template.format(page=page_no)    
    crawler = ListPageCrawler(crawl_method=crawl_method)
    pending_list = crawler.crawl(url)
    logger.info(f"Successfully crawled {len(pending_list)} pending posts.")
    results = []
    for item in pending_list:
        post_id = add_pending_post(engine, item.post_id, item.post_url, list_type.value)
        results.append(post_id)
    return results

def crawl_async(engine, num_pages, crawl_method):
    inputs = []
    for i in range(num_pages):
        inputs.append((engine, i+1, ListType.RENTAL, crawl_method))
        inputs.append((engine, i+1, ListType.SALES, crawl_method))

    pool = ThreadPool(processes=4)
    results = pool.starmap(crawl_page, inputs)
    pool.close()
    pool.join()
    return results

def main(num_pages, crawl_method):
    engine = create_engine(app_config.POSTGRES_CONN)
    results = crawl_async(engine, num_pages, crawl_method)
    success = 0
    fails = 0
    exists = 0
    for result in results:
        for post in result:
            if post == '-1':
                fails += 1
            elif post == '-2':
                exists += 1
            else:
                success += 1
    return {'success': success, 'fails': fails, 'exists': exists}

if __name__ == "__main__":
    results = main(4, crawl_method=CrawlMethod.BASIC)
    print(f"results: {results}")
