import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 設定目標網站
url = "https://www.bbc.com/news"

def fetch_news():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h3')

    news_items = []
    for headline in headlines:
        title = headline.text.strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        news_items.append((title, date))

    return news_items

def save_news_to_db(news_items):
    from .models import News  # 假設你有一個 News 模型

    for title, date in news_items:
        news_item = News(title=title, date=date)
        news_item.save()

