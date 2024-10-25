from typing import List
from lxml import html
from pydantic import BaseModel
from hmd.crawlers.base_crawler import BaseCrawler

class DetailPageData(BaseModel):
    post_title: str
    post_desc: str
    address: str
    last_update: str
    params: dict[str, str]

class DetailPageCrawler(BaseCrawler):
    def crawl(self, url: str) -> List[DetailPageData]:
        html_content = self.get(url)
        tree = html.fromstring(html_content)
        xpath_post_title = "/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div/div[2]/div/h1"
        xpath_post_desc = "/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div/div[4]/div/div[2]/p"
        # xpath_address = "/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div/div[2]/div/div[2]"
        # xpath_address = "/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div/div[2]/div/div[2]/div[1]/span[2]"
        xpath_overview = """//span[contains(@class, "bwq0cbs")]"""
        xpath_params = "/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div/div[3]/div[2]/div[*]"

        post_title = self.extract_text(tree.xpath(xpath_post_title))
        post_desc = self.extract_text(tree.xpath(xpath_post_desc))

        overview = tree.xpath(xpath_overview)
        address = self.extract_text([overview[-2]])
        last_update = self.extract_text([overview[-1]])
        
        params = tree.xpath(xpath_params)
        # Có vài trường hợp nó chỉ show là Cho thuê/Mua bán, nên chỗ này thêm `:` để nó luôn
        # chạy đúng
        params = [(x.text_content()+":").split(":") for x in params]
        params = {x[0]:x[1] for x in params}
        return DetailPageData(
            post_title=post_title,
            post_desc=post_desc,
            address=address,
            last_update=last_update,
            params=params
        )