from typing import Any, List
from lxml import html
from pydantic import BaseModel
from hmd.crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
import re
from datetime import datetime
from hmd.crawlers.utils import *

class DetailPageData(BaseModel):
    post_title: str
    tags: list[str]
    post_desc: str
    address: str
    price_in_mil: float
    last_update: datetime
    params: dict[str, Any]

class DetailPageCrawler(BaseCrawler):
    def crawl(self, url: str) -> List[DetailPageData]:
        html_content = self.get(url)
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        detail_container = soup.find('div', class_=re.compile(r'DetailView_adviewCointainer'))
        
        title_element = detail_container.find('h1')
        title = title_element.get_text(strip=True)

        tag_element = title_element.find_next_sibling()
        tags = tag_element.get_text(strip=True).split('•')

        price_element = tag_element.find_next_sibling()
        price = get_price_in_mil(price_element.get_text(strip=True).split("•")[0])

        address_group = price_element.find_next_sibling()
        span_elements = address_group.find_all("span")
        address = span_elements[0].get_text(strip=True)

        updated_time_str = span_elements[1].get_text(strip=True)
        updated_time = get_update_time(updated_time_str)

        param_container = detail_container.find('div', class_=re.compile(r'AdParam_adParamContainerPty'))
        param_items = param_container.find_all("div", class_=re.compile(r'AdParam_adParamItemPty'))
        # Parse each parameter item into a list of dictionaries
        params = {}
        for item in param_items:
            # Use itemprop attribute as the key if it exists
            key = item.find("strong").get("itemprop")
            value_text = item.find("strong", class_=re.compile(r"AdParam_adParamValuePty")).get_text(strip=True)
            value = parse_value(value_text)
            params[key] = value

        desc_element = detail_container.find('p', class_=re.compile(r"adBody"))
        desc = desc_element.get_text(strip=True)

        return DetailPageData(
            post_title=title,
            tags=tags,
            post_desc=desc,
            address=address,
            price_in_mil=price,
            last_update=updated_time,
            params=params
        )