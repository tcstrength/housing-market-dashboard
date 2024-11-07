import requests
from abc import abstractmethod

class BaseCrawler:
    def get(self, url: str) -> str:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'regionParams={%22regionUrl%22:%22toan-quoc%22%2C%22regionValue%22:0%2C%22regionName%22:%22To%C3%A0n%20qu%E1%BB%91c%22%2C%22subRegionValue%22:0%2C%22subRegionUrl%22:%22%22%2C%22subRegionName%22:%22T%E1%BA%A5t%20c%E1%BA%A3%22%2C%22empty_region%22:false}; showInsertAdOnboarding=true; isOnboardCalFina=true; isOnboardSimilarAd=true; entryPointDetailView=3; __cf_bm=i_QSjOMpfCaDZQt.1b6GMy.MufyUfIdu24PLpX3YKIA-1730946250-1.0.1.1-XG6knHxL7ZIgbbpI5KUdFa7wFHuYCnYhVbbKU42s20N5i41fLNDpb3N.hhijx6rygNxy75dx_nI07yDlBqvG_Q; _cfuvid=pdSJSpQ4RxqyqMjFoVBEj.q_ltgXXCVvqiHQmzUrH9g-1730946250171-0.0.1.1-604800000; cf_clearance=DdwdRfUvcrmoCk1XMrwa9uuFCQf2VOZOg0veU5mMDdA-1730946268-1.2.1.1-fpCvMXbbt1C7l1HlEiBKK7NCJ8W3wt4YjhahTBgFlFay6y32L13aQDgN2UXy17cWcGbYyuB_wt7bw.Dli6l.tYcXtQ4HFaq_3W0c.apQnMv1CwqCyJ_KJtEWiLlkK5BWHxMROg5tkLNuVYP5ig6l2mYIUgIo_aMhBpF_7GwjbwczU5_e.62bRriiaCuhjQ0GjWm16LdqqZ4K.QzBiUXDpLYXyZ2sAFjbWXvTZnW_irw4UFWE.O8aNtHY_urSfAQ03vUX1DKzLvSDjUS9lU0q8bPMQywdr0usNaIa1RHk7asK1d4wCuJwKaVx.CqbQTijO4ctFwc4TOTjq3BPdlonX1yDnT3rjsn6bJwdq6PbCH2tJxwUJYBPC0djZlanGmSy6UGH2kFLrMcbXjUdJbKVVw; countAdPty=5',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        return response.text
    
    def extract_text(self, elms: list):
        text = "".join([x.text_content() for x in elms])
        return text
    
    @abstractmethod
    def crawl(self, url: str):
        pass