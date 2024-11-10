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
        from hmd.jobs.crawl_posts_detail import main
        from airflow.models import Variable
        
        num_crawlers = int(Variable.get("NUM_CRAWLERS", 4))
        num_posts = int(Variable.get("NUM_POSTS", 100))
        results = main(num_posts, num_crawlers)
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