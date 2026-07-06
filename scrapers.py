import time
import json
import requests
from playwright.sync_api import sync_playwright
from database import SessionLocal, TenantDemand
from ai_processor import analyze_rent_content
from config import FB_COOKIE_PATH, FB_GROUP_URL

def save_to_db(data: dict):
    """防重入庫邏輯"""
    db = SessionLocal()
    try:
        # 檢查是否已存在
        exists = db.query(TenantDemand).filter(TenantDemand.post_id == data["post_id"]).first()
        if not exists:
            # 呼叫 AI 進行語意分析
            ai_data = analyze_rent_content(data["raw_content"])
            
            db_item = TenantDemand(
                platform=data["platform"],
                post_id=data["post_id"],
                url=data["url"],
                raw_content=data["raw_content"],
                location=ai_data.get("location"),
                budget_max=ai_data.get("budget_max"),
                room_type=ai_data.get("room_type"),
                identity=ai_data.get("identity")
            )
            db.add(db_item)
            db.commit()
            print(f"[{data['platform'].upper()}] 新增成功: {data['post_id']}")
    except Exception as e:
        print(f"寫入資料庫失敗: {e}")
        db.rollback()
    finally:
        db.close()

def scrape_dcard():
    """Dcard 租屋板 API 抓取"""
    print("開始抓取 Dcard...")
    url = "https://dcard.tw"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        res = requests.get(url, headers=headers)
        posts = res.json()
        for post in posts:
            # 過濾掉房東招租文，只留求租文（可根據標題或標籤特徵過濾）
            title = post.get("title", "")
            content = post.get("excerpt", "")
            full_text = f"{title}\n{content}"
            
            item = {
                "platform": "dcard",
                "post_id": str(post.get("id")),
                "url": f"https://dcard.tw{post.get('id')}",
                "raw_content": full_text
            }
            save_to_db(item)
    except Exception as e:
        print(f"Dcard 抓取異常: {e}")

def scrape_facebook():
    """Facebook 社團 Playwright 模擬 Cookie 抓取"""
    print("開始抓取 Facebook...")
    with sync_playwright() as p:
        # 開啟有頭模式（headless=False）降低被 FB 偵測風險
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 載入 Cookie
        try:
            with open(FB_COOKIE_PATH, "r") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
        except FileNotFoundError:
            print(f"錯誤：找不到 {FB_COOKIE_PATH}。請先使用瀏覽器外掛匯出 Cookie。")
            browser.close()
            return

        page = context.new_page()
        page.goto(FB_GROUP_URL)
        page.wait_for_timeout(5000) # 等待頁面加載
        
        # 模擬向下滾動 3 次以讀取新貼文
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(4000) # 隨機等待，避免被封
            
        # 抓取貼文區塊 (FB 的結構常變動，此為常見的貼文 container 選擇器)
        posts = page.query_selector_all('div[data-ad-preview="message"]')
        
        for idx, post in enumerate(posts):
            text = post.inner_text()
            if not text:
                continue
                
            # 建立簡易的唯一識別碼
            post_id = f"fb_{int(time.time())}_{idx}" 
            
            item = {
                "platform": "facebook",
                "post_id": post_id,
                "url": FB_GROUP_URL,
                "raw_content": text
            }
            save_to_db(item)
            
        browser.close()
