import sys
import pandas as pd
from extractors.vcb_scraper import extract_vcb_exchange_rate
from extractors.tcb_scraper import extract_tcb_exchange_rate
from transformers.cleaner import clean_exchange_rate_data
from db.database import SessionLocal
from db.models import FactExchangeRate

def load_to_postgresql(df):
    """
    Nạp dữ liệu từ Pandas DataFrame vào PostgreSQL.
    Sử dụng logic UPSERT: Nếu đã có dữ liệu của ngày hôm nay thì Cập nhật, chưa có thì Thêm mới.
    """
    if df.empty:
        print("[Loader] Không có dữ liệu để nạp vào Database.")
        return

    print(f"[Loader] Đang nạp {len(df)} bản ghi vào cơ sở dữ liệu...")
    db = SessionLocal()
    
    try:
        # Duyệt qua từng dòng dữ liệu trong DataFrame
        for index, row in df.iterrows():
            # Bước 1: Kiểm tra xem bản ghi này đã tồn tại trong DB chưa
            # (Dựa trên Ràng buộc Unique mới: bank_code + currency_code + record_date)
            existing_record = db.query(FactExchangeRate).filter(
                FactExchangeRate.bank_code == row['bank_code'],
                FactExchangeRate.currency_code == row['currency_code'],
                FactExchangeRate.record_date == row['record_date']
            ).first()

            if existing_record:
                # Bước 2a: Nếu đã tồn tại -> UPDATE giá trị mới nhất
                existing_record.buy_cash = row['buy_cash']
                existing_record.buy_transfer = row['buy_transfer']
                existing_record.sell = row['sell']
                
                # --- CẬP NHẬT THÊM CỘT CHUẨN Ở ĐÂY ---
                existing_record.currency_standard = row['currency_standard']
            else:
                # Bước 2b: Nếu chưa tồn tại -> INSERT bản ghi mới
                new_record = FactExchangeRate(
                    bank_code=row['bank_code'],
                    currency_code=row['currency_code'],
                    
                    # --- THÊM MỚI CỘT CHUẨN Ở ĐÂY ---
                    currency_standard=row['currency_standard'],
                    
                    buy_cash=row['buy_cash'],
                    buy_transfer=row['buy_transfer'],
                    sell=row['sell'],
                    record_date=row['record_date']
                )
                db.add(new_record)
        
        # Bước 3: Lưu lại toàn bộ thay đổi vào Database
        db.commit()
        print("[Loader] Nạp dữ liệu thành công 100%!")

    except Exception as e:
        # Nếu có lỗi, hoàn tác toàn bộ để bảo vệ tính toàn vẹn của database
        db.rollback()
        print(f"[Loader] Lỗi khi nạp dữ liệu: {e}")
    finally:
        # Luôn luôn đóng kết nối để giải phóng bộ nhớ (Connection Pool)
        db.close()

def run_pipeline():
    """Hàm chạy toàn bộ quy trình ETL"""
    print("========== BẮT ĐẦU CHẠY PIPELINE ==========")
    days = 1
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print("[Cảnh báo] Tham số ngày không hợp lệ, chuyển về mặc định 1 ngày.")

    print(f"[Pipeline] Hệ thống sẽ thu thập dữ liệu trong {days} ngày gần nhất.")
    
    # 1. EXTRACT (Truyền số ngày linh hoạt dựa vào tham số đầu vào)
    try:
        vcb_data = extract_vcb_exchange_rate(days) 
    except Exception as e:
        print(f"[Lỗi Extract VCB]: {e}")
        vcb_data = []

    try:
        tcb_data = extract_tcb_exchange_rate(days)
    except Exception as e:
        print(f"[Lỗi Extract TCB]: {e}")
        tcb_data = []   

    # 2. TRANSFORM
    cleaned_df = clean_exchange_rate_data(vcb_data, tcb_data)
    
    # 3. LOAD
    load_to_postgresql(cleaned_df)
    
    print("========== PIPELINE HOÀN THÀNH ==========")

if __name__ == "__main__":
    run_pipeline()