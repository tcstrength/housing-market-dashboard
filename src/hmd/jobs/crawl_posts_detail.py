import json
from loguru import logger
from multiprocessing.pool import ThreadPool
from sqlalchemy import text as sa_text
from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from hmd.core import app_config
from hmd.crawlers.detail_page import DetailPageCrawler
from hmd.crawlers.detail_page import DetailPageData
from hmd.entity.base_entity import BaseEntity
from hmd.entity.pending_post_entity import PendingPostEntity
from hmd.entity.post_detail_entity import PostDetailEntity
from hmd.entity.post_param_entity import PostParamEntity

def get_pending_posts(engine: Engine):
    with Session(engine) as session:
        result = (
            session.query(PendingPostEntity)
            .filter(PendingPostEntity.status == "P")
            .all()
        )
        return result
    
def add_post(engine: Engine, pending_post: PendingPostEntity, data: DetailPageData):
    with Session(engine) as s:
        try:
            detail = PostDetailEntity(
                post_id=pending_post.post_id,
                post_url=pending_post.post_url,
                post_type=pending_post.post_type,
                post_title=data.post_title,
                post_desc=data.post_desc,
                address=data.address,
                tags=json.dumps(data.tags)
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
            logger.info(f"Rollback dued to exception occured.")
            s.rollback()
            raise e

def crawl_one_pending(engine: Engine, pending_post: PendingPostEntity):
    post_url = pending_post.post_url
    crawler = DetailPageCrawler()
    try:
        data = crawler.crawl(post_url)
        add_post(engine, pending_post, data)
    except Exception as e:
        logger.warning(e)

def crawl_pending_posts(engine: Engine):
    pending_posts = get_pending_posts(engine)
    inputs = []
    for pending_post in pending_posts:
        inputs.append((engine, pending_post))

    pool = ThreadPool(processes=8)
    pool.starmap(crawl_one_pending, inputs)
    pool.close()
    pool.join()

if __name__ == "__main__":
    engine = create_engine(app_config.POSTGRES_CONN)
    BaseEntity.metadata.create_all(
        engine, tables=[
            PostDetailEntity.__table__,
            PostParamEntity.__table__
        ]
    )
    crawl_pending_posts(engine)
    # update_pending_status(engine, 120631145, "S")