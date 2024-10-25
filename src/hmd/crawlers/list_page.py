import re
from typing import List
from lxml import html
from urllib.parse import urlparse
from pydantic import BaseModel
from hmd.crawlers.base_crawler import BaseCrawler

class ListPageData(BaseModel):
    post_url: str
    post_id: str

class ListPageCrawler(BaseCrawler):
    def crawl(self, url: str) -> List[ListPageData]:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        html_content = self.get(url)
        tree = html.fromstring(html_content)
        urls = tree.xpath('//a/@href')
        filtered_urls = [url for url in urls if re.search(r"(mua-ban.+\.htm)", url)]
        filtered_urls = list(set(filtered_urls))
        result = []
        for url in filtered_urls:
            match = re.search(r"(mua-ban.+\/)(\d+).htm", url)
            if match:
                if url.startswith("/"): 
                    url = f"{base_url}{url}"
                result.append(ListPageData(post_url=url, post_id=match.group(2)))
        return result
        