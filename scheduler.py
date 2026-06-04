from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from main_etl import run_pipeline
import datetime

def job_wrapper():
    """Hàm bọc lại pipeline để in thêm thời gian chạy log"""
    print(f"\n[{datetime.datetime.now()}] ĐANG KHỞI ĐỘNG LUỒNG ETL TỰ ĐỘNG...")
    run_pipeline()
    print(f"[{datetime.datetime.now()}] ĐÃ HOÀN THÀNH LUỒNG ETL.\n")

if __name__ == "__main__":
    # Khởi tạo bộ đặt lịch
    scheduler = BlockingScheduler()
    # Cấu hình 1: Chạy tự động vào lúc 8:00 sáng và 16:00 chiều mỗi ngày từ Thứ 2 đến Thứ 6
    scheduler.add_job(
        job_wrapper,
        CronTrigger(day_of_week='mon-fri', hour='9,18', minute='0'),
        id='banking_etl_job',
        name='Daily Banking ETL'
    )
    print("========== HỆ THỐNG LÊN LỊCH ĐÃ KHỞI ĐỘNG ==========")
    print("Các Job đã được cấu hình:")
    for job in scheduler.get_jobs():
        print(f"- {job.name} (Chạy vào: {job.trigger})")
    print("Nhấn Ctrl+C để thoát...\n")
    # Để test code NGAY LẬP TỨC mà không cần đợi đến 8h sáng, 
    # hãy mở comment (xóa dấu #) ở dòng dưới đây để chạy mồi 1 lần:
    # job_wrapper()
    # Bắt đầu vòng lặp vô hạn để giữ chương trình luôn chạy ngầm
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Đã tắt hệ thống lên lịch.")