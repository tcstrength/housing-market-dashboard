import time
import pendulum
from airflow.decorators import dag, task
from common.common import default_args, tz_string

@dag(
    start_date=pendulum.datetime(2024, 1, 1, tz=tz_string),
    catchup=False,
    schedule_interval="30 7 * * *",
    default_args=default_args,
    tags=["chotot"],
)
def get_pending_posts():

    @task
    def crawl_posts():
        from hmd.jobs.crawl_pending_posts import main
        from airflow.models import Variable
        num_pages = int(Variable.get("NUM_PAGES", 4))
        results = main(num_pages)
        return results

    @task
    def report(results):
        from common.telegram_api import send_message

        success = 0
        fails = 0
        for result in results:
            for post in result:
                if post == '-1':
                    fails += 1
                else:
                    success += 1
        print(f"Success: {success}")
        print(f"Fails: {fails}")

        send_message(f"Get pending posts:\n    Total: {success + fails}\n    Success: {success}\n    Fails: {fails}")

    report(crawl_posts())

get_pending_posts()