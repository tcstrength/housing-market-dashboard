import requests
from abc import abstractmethod

class BaseCrawler:
    def get(self, url: str) -> str:
        headers = {
            'Cookie': '__cf_bm=Zpj517BshmxzfQuGgkaKB8oFtcqai640BtGnm5gk_rA-1730978939-1.0.1.1-8d39pS.3DpTHWNsudRr.T9qpyMMOynftE8NLF26hpFoXX51Rp3RXXc_j8nCDbjOOeFiCsGAWXQHpOuenh6rELg; _cfuvid=m3LgkYW3uNpP_4uheb.RZ6I9GmaIz2fZpsrbW4Iu2kc-1730978939432-0.0.1.1-604800000',
            'User-Agent': 'PostmanRuntime/7.42.0',
            'Cache-Control': 'no-cache',
            'Accept': "*/*",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        response = requests.get(url, headers=headers)
        # Store the context to retrieve and log if error occurs
        self._ctx_html_content = response.text
        return self._ctx_html_content
    
    def extract_text(self, elms: list):
        text = "".join([x.text_content() for x in elms])
        return text
    
    @abstractmethod
    def crawl(self, url: str):
        pass