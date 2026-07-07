import os

# 資料庫連線設定 (請替換為您的 PostgreSQL 帳密與資料庫名稱)
DATABASE_URL = "postgresql://username:password@localhost:5432/rent_db"

# OpenAI API 金鑰
OPENAI_API_KEY = "your-openai-api-key-here"

# Facebook 相關設定
FB_COOKIE_PATH = "fb_cookies.json"  # 瀏覽器匯出的 Cookie 檔案路徑
FB_GROUP_URLS = [
    "https://www.facebook.com/groups/2391145197642950", # 台北租屋社團🌻
    "https://www.facebook.com/groups/464870710346711", # 台北租屋、出租專屬社團
    "https://www.facebook.com/groups/459966811445588", # 台北租屋、出租專屬平台 2.0
    "https://facebook.com/groups/313385739282042", # 大台北好好租屋🪴未看屋前匯款都是詐騙
    "https://www.facebook.com/groups/227082894440964", # 中和、永和、板橋租屋資訊
    "https://www.facebook.com/groups/359576301158357", # 大台北好好好租屋網（含新北市）
    "https://www.facebook.com/groups/1040396368050817", # 台北租屋 新北租屋｜租屋補助・社會住宅・免仲介費・屋主自租
    "https://www.facebook.com/groups/1513936138926333", # 新北租屋、出租專屬社團
    "https://www.facebook.com/groups/939218550146090", # 雙北【租屋市集】雅房、套房、獨立套房、分租套房、共生公寓
    "https://www.facebook.com/groups/3140810842843485", # 板橋租屋網 我是好房東
    "https://www.facebook.com/groups/1454032725691534", # 台北市、新北市 租屋 房東、房客資訊分享平台
    "https://www.facebook.com/groups/2032594816953477", # 大台北找租出租屋
    "https://www.facebook.com/groups/161099969025675", # 雙北-整層/套房 租屋網 (有房出租盡量PO)
    "https://www.facebook.com/groups/388722468446960", # 台北租屋出租社團
    "https://www.facebook.com/groups/978101552379651", # 房東社團-全台最多屋主自租-雙北租屋尋屋找屋最快
    "https://www.facebook.com/groups/1151927161997283", # 台北新北租屋◆房東房客盡量PO
    "https://www.facebook.com/groups/1513612272293611", # 大台北租屋
    "https://www.facebook.com/groups/221614965050605", # Apartment Rentals In Taiwan Short-term And Longterm Leases Available 台北租屋
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    "https://facebook.com",
    
]
# 您監控的社團網址
