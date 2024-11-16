import time
import pendulum
from airflow.decorators import dag, task
from common.common import default_args, tz_string
from airflow.operators.python import get_current_context

@dag(
    start_date=pendulum.datetime(2024, 1, 1, tz=tz_string),
    catchup=False,
    schedule_interval="30 7 * * *",
    default_args=default_args,
    tags=["chotot"],
)
def get_detail_posts():
    @task
    def get_pending_posts_task():
        from hmd.jobs.crawl_posts_detail import get_pending_posts
        from airflow.models import Variable
        import json

        num_posts = int(Variable.get("NUM_POSTS", 100))
        posts = get_pending_posts(num_posts)
        return [json.dumps(post.to_dict()) for post in posts]
    
    @task(map_index_template="{{ post_id }}")
    def crawl_detail_post(post):
        from hmd.crawlers.base_crawler import CrawlMethod
        from hmd.jobs.crawl_posts_detail import crawl_one_pending
        from airflow.models import Variable
        import json
        from hmd.entity.pending_post_entity import PendingPostEntity

        crawl_method = Variable.get("CrawlMethod", 'FLARESOLVERR')
        context = get_current_context()
        post_data = json.loads(post)
        post_obj = PendingPostEntity.from_dict(post_data)
        post_id = post_obj.post_id
        context["post_id"] = post_id
        result = crawl_one_pending(post_obj, CrawlMethod[crawl_method])
        return result

    @task
    def report(results):
        from common.telegram_api import send_message

        success = 0
        fails = 0
        for post in results:
            if post == "-1":
                fails += 1
            else:
                success += 1
        print(f"Success: {success}")
        print(f"Fails: {fails}")

        send_message(f"Get detail posts:\n    Total: {success + fails}\n    Success: {success}\n    Fails: {fails}")

    pending_posts = get_pending_posts_task()
    results = crawl_detail_post.expand(post=pending_posts)

    report(results)

get_detail_posts()