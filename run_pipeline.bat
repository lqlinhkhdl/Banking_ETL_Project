@echo off
cls
echo ===================================================================
echo [Anaconda Automation] Dang kich hoat moi truong 'scraping'...
echo ===================================================================

:: 1. Gọi file kích hoạt gốc của Anaconda
call "C:\Users\lee\anaconda3\Scripts\activate.bat" "C:\Users\lee\anaconda3"

:: 2. Kích hoạt đúng môi trường ảo 'scraping' của bạn
call conda activate scraping

echo [OK] Da kich hoat moi truong 'scraping' thanh cong!
echo Chuan bi di chuyen vao thu muc du an...
timeout /t 2 > nul

:: 3. Di chuyển vào thư mục dự án của bạn
cd /d "D:\Data\project\banking_etl_project"

echo ===================================================================
echo [ETL Scheduler] KICH HOAT BO HEN GIO TU DONG AP-SCHEDULER
echo ===================================================================
echo He thong dang chuan bi kich hoat Bo dat lich, vui long quan sat...
timeout /t 3

:: 4. THAY ĐỔI Ở ĐÂY: Chạy file hẹn giờ thay vì chạy file ETL trực tiếp
python scheduler_control.py

echo.
echo ===================================================================
echo [CANH BAO] He thong hen gio da bi ngat hoac gap loi!
echo ===================================================================
echo [CHU Y] Cua so nay se GIU NGUYEN de ban kiem tra nhat ky (Logs).
echo Hay bam nut dau [X] o goc tren ben phai de dong cua so nay hoac bam nut bat ky.
echo ===================================================================
echo.

:: Giữ cửa sổ đứng im nếu lỡ may bộ hẹn giờ bị sập/tắt đột ngột
pause