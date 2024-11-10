import requests
from enum import Enum
from abc import abstractmethod

class CrawlMethod(Enum):
    FLARESOLVERR = "flaresolverr"
    BASIC = "basic"

class BaseCrawler:
    def __init__(
        self,
        crawl_method: CrawlMethod = CrawlMethod.BASIC,
        flaresolverr_url: str = None
    ):
        self._crawl_method = crawl_method
        if self._crawl_method == CrawlMethod.FLARESOLVERR:
            self._flaresolverr_url = flaresolverr_url
            if flaresolverr_url is None:
                raise ValueError((
                    f"The crawl method is {crawl_method}, "
                    "the `flaresolverr_url` must not be None."
                ))
            
            print(self._flaresolverr_url)
        
    def get(self, url: str) -> str:
        if self._crawl_method == CrawlMethod.BASIC:
            result = self.__get_basic(url)
        if self._crawl_method == CrawlMethod.FLARESOLVERR:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Cache-Control': 'no-cache',
            'Accept': "*/*",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        response = requests.get(url, headers=headers)
        return response.text
    
    def extract_text(self, elms: list):
        text = "".join([x.text_content() for x in elms])
        return text
    
    @abstractmethod
    def crawl(self, url: str):
        pass

if __name__ == "__main__":
    from hmd.core import app_config
    url = "https://www.nhatot.com/thue-nha-dat-quan-binh-tan-tp-ho-chi-minh/120623332.htm"
    crawler = BaseCrawler(CrawlMethod.FLARESOLVERR, app_config.FLARESOLVERR_URL)
    crawler.get(url)