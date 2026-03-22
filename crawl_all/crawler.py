# =============================
# import 區（工具準備）
# =============================
import os
import json
import requests
from bs4 import BeautifulSoup
# =============================
# 路徑設定 (避免路徑錯誤)
# =============================
# crawler目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 專案根目錄
PROJECT_DIR = os.path.join(BASE_DIR, "..")
#
print("Crawler directory:", BASE_DIR)
print("Project directory:", PROJECT_DIR)
# headers（避免被網站擋）
headers = {"User-Agent": "Mozilla/5.0"}
# =============================
# 核心函式
# =============================
def crawl_site(config):
    # 顯示目前爬哪個網站
    print(f"🚀 開始爬取 {config['name']}")
    # 發request,設定編碼
    res = requests.get(config["url"], headers=headers, timeout=20)
    res.encoding = "utf-8"
    # HTML → DOM,類似 JS,document.querySelector()
    soup = BeautifulSoup(res.text, "html.parser")
    # 找外層 container
    news_container = soup.find(
        config["container_tag"], class_=config["container_class"]
    )
    #找每一筆 item
    items = (
        news_container.find_all(config["item_tag"], class_=config["item_class"])[:10]
        if news_container
        else []
    )
    #建立資料容器
    news_list = []
    #逐筆處理
    for item in items:
        # link
        a_tag = item.find("a")
        href = a_tag.get("href") if a_tag else None
        #
        if config["link_prefix"]:
            link = config["link_prefix"] + href if href else "❌ 無連結"
        else:
            link = href if href else "❌ 無連結"
        # image
        img_tag = item.find("img")
        img_url = (
            (img_tag.get("data-original") or img_tag.get("src"))
            if img_tag
            else "❌ 無圖片"
        )
        # title
        title_tag = item.find(config["title_tag"], class_=config.get("title_class"))
        title = title_tag.get_text(strip=True) if title_tag else "❌ 無標題"
        #存資料
        news_list.append(
            {
                "title": title,
                "link": link,
                "image": img_url,
            }
        )
    #輸出 JSON
    output_dir = os.path.join(os.path.dirname(__file__), "..", config["folder"])
    #output_dir, exist_ok=True,如果資料夾不存在 → 自動建立 
    os.makedirs(output_dir, exist_ok=True)
    #組完整檔案路徑
    output_path = os.path.join(output_dir, config["output"])
    #寫入 JSON,ensure_ascii=False,中文正常
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    #完成
    print(f"✅ 完成 {config['name']}")
# =============================
# 各網站設定
# =============================
sites = [
    #
    {
        # 網站名稱 + 網址
        "name": "ETtoday",
        "url": "https://game.ettoday.net/focus-2.php?topicId=333",
        # 外層區塊
        "container_tag": "div",
        "container_class": "block_1",
        # 每一筆新聞
        "item_tag": "div",
        "item_class": "box clearfix",
        # 標題位置
        "title_tag": "h3",
        "title_class": None,
        # 補網址
        "link_prefix": "",
        # 輸出位置
        "folder": "ettoday",
        "output": "ettoday_data.json",
    },
    #
    {
        "name": "GameApps",
        "url": "https://www.gameapps.hk/news",
        "container_tag": "div",
        "container_class": "col-xs-8",
        "item_tag": "div",
        "item_class": "media news-big-icon",
        "title_tag": "h3",
        "title_class": "media-heading",
        "link_prefix": "https://www.gameapps.hk",
        "folder": "gameapps",
        "output": "gameapps_data.json",
    },
    #
    {
        "name": "SETN",
        "url": "https://esport.setn.com/viewall",
        "container_tag": "div",
        "container_class": "conArea",
        "item_tag": "div",
        "item_class": "conBox newsItems",
        "title_tag": "h3",
        "title_class": None,
        "link_prefix": "https://esport.setn.com",
        "folder": "setn",
        "output": "setn_data.json",
    },
]
# =============================
# 主程式
# =============================
if __name__ == "__main__":
    for site in sites:
        crawl_site(site)
    print("\n🎉 全部新聞爬取完成")
# 
"""
========================================================
Architecture note
========================================================
--------------------------------------------------------
Data Source
--------------------------------------------------------
-------------
Target Websites (HTML)
- ETtoday
- GameApps
- Setn
-------------
Output
- JSON files
  {
    title: string,
    link: string,
    image: string
  }
--------------------------------------------------------
System Flow
--------------------------------------------------------
-----------------
Main Entry
-----------------
__main__
  ↓
for site in sites
  ↓
crawl_site(config)
--------------------------------------------------------
Crawler Flow
--------------------------------------------------------
crawl_site(config)
  ↓
HTTP Request (requests.get)
  ↓
HTML → DOM (BeautifulSoup)
  ↓
find container
  ↓
find items (limit 10)
  ↓
loop items
  ↓
extract
  - title
  - link
  - image
  ↓
append → news_list[]
  ↓
write JSON file
--------------------------------------------------------
State (inside crawl_site)
--------------------------------------------------------
config
  current site configuration
----------
-----------------
news_container
  HTML container block
-----------------
items
  list of news DOM elements
-----------------
news_list
  final structured data
--------------------------------------------------------
Core Functions
--------------------------------------------------------
crawl_site(config)
  main crawler logic
-----------------
requests.get()
  fetch HTML
-----------------
BeautifulSoup()
  parse DOM
-----------------
find / find_all
  extract elements
-----------------
json.dump()
  output structured data
-----------------
--------------------------------------------------------
Configuration Design
--------------------------------------------------------
sites[]
  list of crawler configs
-----------------
each config includes:
  - name
  - url
  - container selector
  - item selector
  - title selector
  - link prefix
  - output path
👉 same crawler logic
👉 different config
👉 reusable system
--------------------------------------------------------
System Concept (重要🔥)
--------------------------------------------------------
Data Pipeline（資料流）
Website HTML
  ↓
Crawler (Python)
  ↓
JSON
  ↓
Frontend (GameNews)










































"""