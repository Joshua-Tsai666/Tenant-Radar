from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TenantDemand(Base):
    __tablename__ = "tenant_demands"

    # 使用 platform + post_id 作為複合唯一鍵，防重複
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)        # 'facebook' 或 'dcard'
    post_id = Column(String(100), unique=True, nullable=False) 
    url = Column(String(500))
    raw_content = Column(Text)                           # 原始全文
    
    # 以下為 AI 結構化後的欄位
    location = Column(String(100))                       # 租屋地點
    budget_max = Column(Integer)                         # 預算上限
    room_type = Column(String(100))                      # 房型
    identity = Column(String(100))                       # 租客身分
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 建立資料表
Base.metadata.create_all(bind=engine)
