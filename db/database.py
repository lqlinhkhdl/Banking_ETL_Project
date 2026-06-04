import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv()

# Lấy chuỗi kết nối Database
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")
# Khởi tạo Engine (Động cơ lõi quản lý kết nối)
# Thêm cờ client_encoding để ép Python giao tiếp chuẩn qua TCP/IP trên Windows
engine = create_engine(DATABASE_URL, connect_args={"client_encoding": "utf8"})

# Khởi tạo Session (Phiên làm việc để thực hiện các lệnh Insert/Update)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class để các file Models kế thừa
Base = declarative_base()

def get_db():
    """Hàm này sẽ được dùng để cấp session cho các module khác"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()