import json
import traceback
from loguru import logger
from multiprocessing.pool import ThreadPool
from sqlalchemy import text as sa_text
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from hmd.core import app_config
from hmd.crawlers.base_crawler import CrawlMethod
from hmd.crawlers.detail_page import DetailPageCrawler
from hmd.crawlers.detail_page import DetailPageData
from hmd.entity.base_entity import BaseEntity
from hmd.entity.pending_post_entity import PendingPostEntity
from hmd.entity.crawl_error_entity import CrawlErrorEntity
from hmd.entity.post_detail_entity import PostDetailEntity
from hmd.entity.post_param_entity import PostParamEntity
from sqlalchemy.orm import sessionmaker

def get_pending_posts(engine, limit):
    logger.info(f"Retrieve up to {limit} pending posts.")
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    result = None
    try:
        result = (
            session.query(PendingPostEntity)
            .filter(PendingPostEntity.status == "P")
            .limit(limit)
            .all()
        )
    finally:
        # Close the session
        session.close()
    return result
    
def add_post(engine, pending_post: PendingPostEntity, data: DetailPageData):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    s = SessionLocal()
    try:
        detail = PostDetailEntity(
            post_id=pending_post.post_id,
            post_url=pending_post.post_url,
            post_type=pending_post.post_type,
            post_title=data.post_title,
            post_desc=data.post_desc,
            address=data.address,
            price_in_mil=data.price_in_mil,
            tags=json.dumps(data.tags),
            posted_at=int(data.last_update.timestamp())
        )

        tab = pending_post.__table__.name
        stmt = f"UPDATE {tab} SET status = 'S' WHERE post_id = {pending_post.post_id}"
        s.execute(sa_text(stmt))

        params = []
        for k, v in data.params.items():
            param = PostParamEntity(
                post_id=pending_post.post_id,
                param_key=k,
                param_value=v
            )
            params.append(param)
        s.add(detail)
        s.add_all(params)
        s.commit()
    except Exception as e:
            logger.info(f"Rollback issued due to exception occured.")
            s.rollback()
            raise e
    finally:
        s.close()

def crawl_one_pending(engine, pending_post: PendingPostEntity):
    post_url = pending_post.post_url
    post_id = pending_post.post_id
    logger.info(f"Crawl {post_url}...")
    crawler = DetailPageCrawler(
        crawl_method=CrawlMethod.FLARESOLVERR,
        flaresolverr_url=app_config.FLARESOLVERR_URL
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    s = SessionLocal()
    result = None
    try:
        exist = (
            s.query(PostDetailEntity)
            .filter(PostDetailEntity.post_id == post_id)
            .count()
        )

        if exist > 0:
            logger.info(f"PostDetail `{post_id}` already exists")
        else:
            data = crawler.crawl(post_url)
            add_post(engine, pending_post, data)
            logger.info(f"Crawled PostDetail `{post_id}` successfully.")
            result = post_id
    except Exception as e:
        trace_str = traceback.format_exc()
        log = CrawlErrorEntity(
            post_id=post_id,
            crawl_error=trace_str,
            html_content=crawler._ctx_html_content
        )
        s.add(log)
        s.flush()
        s.refresh(log)
        s.expunge(log)
        logger.warning(f"Failed to crawl PostDetail `{post_id}`, url={post_url}, for more details, please check out the log with id=`{log.log_id}`")
        tab = pending_post.__table__.name
        stmt = f"UPDATE {tab} SET status = 'E' WHERE post_id = {post_id}"
        s.execute(sa_text(stmt))
        s.commit()
    finally:
        s.close()
    return result

def crawl_async(engine, num_posts, num_crawlers):
    pending_posts = get_pending_posts(engine, num_posts, num_crawlers)
    inputs = []
    for pending_post in pending_posts:
        inputs.append((engine, pending_post))

    pool = ThreadPool(processes=num_crawlers)
    results = pool.starmap(crawl_one_pending, inputs)
    pool.close()
    pool.join()
    return results

def main(num_posts: int, num_crawlers: int = 4):
    engine = create_engine(app_config.POSTGRES_CONN)
    BaseEntity.metadata.create_all(
        engine, tables=[
            PostDetailEntity.__table__,
            PostParamEntity.__table__,
            CrawlErrorEntity.__table__
        ]
    )
    results = crawl_async(engine, num_posts=num_posts, num_crawlers=num_crawlers)
    return results

if __name__ == "__main__":
    main(1)
    