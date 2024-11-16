import requests
from abc import abstractmethod
from loguru import logger
from hmd.core import app_config

class CrawlMethod(Enum):
    FLARESOLVERR = "flaresolverr"
    BASIC = "basic"

class BaseCrawler:
    def __init__(
        self,
        crawl_method: CrawlMethod = CrawlMethod.BASIC
    ):
        self._crawl_method = crawl_method
        if self._crawl_method == CrawlMethod.FLARESOLVERR:
            self._flaresolverr_url = app_config.FLARESOLVERR_URL
            logger.debug(f"Use flaresolverr={self._flaresolverr_url}")
        
    def get(self, url: str) -> str:
        if self._crawl_method == CrawlMethod.BASIC:
            result = self.__get_basic(url)
        elif self._crawl_method == CrawlMethod.FLARESOLVERR:
            result = self.__get_with_flare_solverr(url)
        else:
            raise ValueError("The input `method` is invalid.")
        
        self._ctx_html_content = result
        return self._ctx_html_content
    
    def __get_with_flare_solverr(self, url: str) -> str:
        response = requests.post(
            f"{self._flaresolverr_url}",
            json={
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 60000,
            },
        )
        response_data = response.json()

        if response_data.get("status") == "ok":
            return response_data.get("solution").get("response")
        else:
            return f"Failed to bypass: {response_data}"

    def __get_basic(self, url: str) -> str:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://google.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1' 
        }
        response = requests.get(url, headers=headers)
        return response.text
    
    def extract_text(self, elms: list):
        text = "".join([x.text_content() for x in elms])
        return text
    
    @abstractmethod
    def crawl(self, url: str):
        pass