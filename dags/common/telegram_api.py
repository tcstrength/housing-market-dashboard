import os
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_API_KEY=os.getenv("TELEGRAM_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={message}"
    return requests.get(url).json()

if __name__ == "__main__":
    message = "I'm a bot, please talk to me!"
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={message}"
    print(requests.get(url).json())