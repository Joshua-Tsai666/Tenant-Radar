import os

# 資料庫連線設定 (請替換為您的 PostgreSQL 帳密與資料庫名稱)
DATABASE_URL = "postgresql://username:password@localhost:5432/rent_db"

# OpenAI API 金鑰
OPENAI_API_KEY = "your-openai-api-key-here"

# Facebook 相關設定
FB_COOKIE_PATH = "fb_cookies.json"  # 瀏覽器匯出的 Cookie 檔案路徑
FB_GROUP_URL = "https://facebook.com"  # 您想監控的社團網址
