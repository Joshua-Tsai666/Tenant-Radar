from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import threading
import time
from database import SessionLocal, TenantDemand
import scrapers

app = FastAPI(title="租客需求抓取系統 API")

# 允許前端網站跨網域存取 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 接口：供您的前端網站撈取最新租客需求
@app.get("/api/demands")
def get_demands(limit: int = 20, db: Session = Depends(get_db)):
    """獲取最新的租客需求，支援由新到舊排序"""
    return db.query(TenantDemand).order_by(TenantDemand.created_at.desc()).limit(limit).all()

# 背景排程：每 2 小時自動抓取一次
def run_scrapers_loop():
    while True:
        print("--- 定時爬蟲任務啟動 ---")
        scrapers.scrape_dcard()
        scrapers.scrape_facebook()
        print("--- 任務結束，等待下次執行 ---")
        time.sleep(7200) # 7200 秒 = 2 小時

@app.on_event("startup")
def startup_event():
    # 伺服器啟動時，自動在背景開一個執行緒跑爬蟲排程
    threading.Thread(target=run_scrapers_loop, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
