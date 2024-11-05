import requests
from abc import abstractmethod

class BaseCrawler:
    def get(self, url: str) -> str:
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