import time
from hmd.jobs.crawl_pending_posts import ListType
import pendulum
from airflow.decorators import dag, task
from common.common import default_args, tz_string
from airflow.operators.python import get_current_context

@dag(
    start_date=pendulum.datetime(2024, 1, 1, tz=tz_string),
    catchup=False,
    schedule_interval="0 7 * * *",
    default_args=default_args,
    tags=["chotot"],
)
def get_pending_posts():

    @task
    def prepared_inputs():
        from airflow.models import Variable
        num_pages = int(Variable.get("NUM_PAGES", 4))
        inputs = []
        for i in range(num_pages):
            inputs.append(i+1)
        return inputs

    @task(map_index_template="{{ page_no }}")
    def crawl_posts(page_no, type):
        from hmd.jobs.crawl_pending_posts import crawl_page
        from hmd.crawlers.base_crawler import CrawlMethod
        from airflow.models import Variable

        crawl_method = Variable.get("CrawlMethod", 'FLARESOLVERR')
        context = get_current_context()
        context["page_no"] = f"{type}-{page_no}"
        results = crawl_page(page_no, type, CrawlMethod[crawl_method])
        return results

    @task(trigger_rule='none_failed')
    def report(results):
        from common.telegram_api import send_message
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
        total = success + fails + exists
        send_message(f"Get pending posts:\n    Total: {total}\n    Success: {success}\n    Fails: {fails}\n    Exists: {exists}")

    inputs = prepared_inputs()
    results = crawl_posts.partial(type=ListType.RENTAL).expand(page_no=inputs)
    report(results)

get_pending_posts()