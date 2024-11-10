import time
import pendulum
from airflow.decorators import dag, task
from common.common import default_args, tz_string

@dag(
    start_date=pendulum.datetime(2024, 1, 1, tz=tz_string),
    catchup=False,
    schedule_interval="30 8 * * *",
    default_args=default_args,
    tags=["chotot"],
)
def get_detail_posts():

    @task
    def crawl_detail_posts():
        from src.hmd.core.app_config import POSTGRES_CONN
        from src.hmd.entity.base_entity import BaseEntity
        from src.hmd.entity.post_detail_entity import PostDetailEntity
        from src.hmd.entity.post_param_entity import PostParamEntity
        from sqlalchemy import create_engine
        from hmd.jobs.crawl_posts_detail import crawl_async
        from airflow.models import Variable

        num_posts = int(Variable.get("NUM_POSTS", 300))
        engine = create_engine(POSTGRES_CONN)
        BaseEntity.metadata.create_all(
            engine, tables=[
                PostDetailEntity.__table__,
                PostParamEntity.__table__
            ]
        )
        results = crawl_async(engine, limit=num_posts)
        return results

    @task
    def report(results):
        from common.telegram_api import send_message

        success = 0
        fails = 0
        for post in results:
            if post == '-1':
                fails += 1
            else:
                success += 1
        print(f"Success: {success}")
        print(f"Fails: {fails}")

        send_message(f"Get detail posts:\n    Total: {success + fails}\n    Success: {success}\n    Fails: {fails}")

    report(crawl_detail_posts())

get_detail_posts()