# Banking ETL Project

Hệ thống ETL (Extract, Transform, Load) tự động để thu thập, làm sạch và lưu trữ dữ liệu tỷ giá ngoại tệ từ các ngân hàng Việt Nam.

---

## Mục Đích Dự Án

Dự án này được thiết kế để:

- **Trích xuất (Extract)** dữ liệu tỷ giá ngoại tệ từ các ngân hàng Vietcombank (VCB) và Techcombank (TCB)
- **Chuyển đổi (Transform)** dữ liệu thô thành định dạng chuẩn hóa, sạch sẽ
- **Nạp (Load)** dữ liệu vào PostgreSQL Database sử dụng logic UPSERT (Update/Insert)
- **Lên lịch tự động (Schedule)** chạy pipeline vào lúc 9:00 AM và 18:00 PM từ Thứ 2 đến Thứ 6 (nếu không muốn chạy thì vào comment "::" trong file bat )

---

## Cấu Trúc Dự Án

```
banking_etl_project/
├── main_etl.py                 # Entry point chính - chứa hàm run_pipeline()
├── scheduler.py                # Cấu hình lên lịch tự động (APScheduler)
├── run_pipeline.bat            # Script chạy dự án trên Windows
├── .env                        # Biến môi trường (DATABASE_URL)
├── .gitignore                  # Git ignore file
│
├── db/                         # Lớp quản lý Database
│   ├── database.py             # Kết nối PostgreSQL, SessionLocal, Base model
│   ├── models.py               # SQLAlchemy models (DimBank, FactExchangeRate)
│
├── extractors/                 # Lớp trích xuất dữ liệu
│   ├── vcb_scraper.py          # Scraper cho Vietcombank (API + XML)
│   ├── tcb_scraper.py          # Scraper cho Techcombank (API)
│   ├── vnstock_api.py          # (Tùy chọn) API cho dữ liệu chứng khoán
│
├── transformers/               # Lớp chuyển đổi/làm sạch dữ liệu
│   ├── cleaner.py              # Gộp, chuẩn hóa, làm sạch dữ liệu
│
├── database/                   # SQL migration scripts
│   ├── 0.sql                   # Khởi tạo schema ban đầu
│   ├── 1.sql                   # Migration 1
│   ├── 2.sql                   # Migration 2
│   ├── 3.sql                   # Migration 3
│
└── Book1.twb                   # Tableau workbook (dashboard visualization)
```

---

## Công Nghệ Sử Dụng

### Backend & Data Processing
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|-----------|---------|
| **Python** | 3.9+ | Ngôn ngữ lập trình chính |
| **SQLAlchemy** | 1.4+ | ORM cho PostgreSQL |
| **pandas** | 1.3+ | Xử lý & chuyển đổi dữ liệu |
| **requests** | 2.28+ | Scraping API từ website ngân hàng |
| **APScheduler** | 3.10+ | Lên lịch tự động (cron job) |
| **python-dotenv** | 0.20+ | Quản lý biến môi trường |

### Database
| Công Nghệ | Chi Tiết |
|-----------|---------|
| **PostgreSQL** | 12+ - Database lưu trữ tỷ giá |
| **SQLAlchemy ORM** | Quản lý schema & relationships |

### Data Source
| Nguồn | API/Endpoint | Dữ Liệu |
|------|------------|--------|
| **Vietcombank (VCB)** | `https://www.vietcombank.com.vn/api/exchangerates` | Tỷ giá tiền tệ |
| **Techcombank (TCB)** | `https://techcombank.com/...exchange-rates...` | Tỷ giá tiền tệ |

### Visualization
| Công Nghệ | Mục Đích |
|-----------|---------|
| **Tableau** | Dashboard trực quan hóa dữ liệu tỷ giá |

---

## Hướng Dẫn Cài Đặt & Chạy

### Yêu Cầu Hệ Thống

- **Python**: 3.9 trở lên
- **PostgreSQL**: 12 trở lên
- **pip**: Package manager cho Python
- **Anaconda** (tùy chọn): Môi trường quản lý Python

### Chuẩn Bị Database

#### Bước 1: Kết nối tới PostgreSQL
```bash
psql -U postgres
```

#### Bước 2: Tạo Database
```sql
CREATE DATABASE banking_dw;
```

#### Bước 3: Chạy Migration Scripts
```bash
psql -U postgres -d banking_dw -f database/0.sql
psql -U postgres -d banking_dw -f database/1.sql
psql -U postgres -d banking_dw -f database/2.sql
psql -U postgres -d banking_dw -f database/3.sql
```

### Cài Đặt Python Dependencies

#### Phương pháp 1: Sử dụng Anaconda (Khuyến nghị)
```bash
# Tạo môi trường ảo
conda create --name scraping python=3.9

# Kích hoạt môi trường
conda activate scraping

# Cài đặt thư viện yêu cầu
pip install -r requirements.txt
```

#### Phương pháp 2: Sử dụng pip
```bash
pip install sqlalchemy pandas requests apscheduler python-dotenv
```

### Cấu Hình Biến Môi Trường

Tạo file `.env` tại thư mục gốc dự án:
```env
DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/banking_dw
```

**Thay thế:**
- `password` → mật khẩu PostgreSQL của bạn
- `127.0.0.1` → host PostgreSQL (mặc định localhost)
- `5432` → port PostgreSQL (mặc định 5432)

### Chạy Dự Án

#### Cách 1: Chạy Pipeline Một Lần (Manual)
```bash
python main_etl.py
```

#### Cách 2: Chạy Scheduler Tự Động (Windows)
```bash
run_pipeline.bat
```

Hoặc chạy trực tiếp từ Terminal:
```bash
python scheduler.py
```

**Lưu ý**: Scheduler sẽ chạy tự động vào:
- ⏰ 8:00 AM (08:00)
- ⏰ 4:00 PM (16:00)
- 📅 Từ Thứ 2 đến Thứ 6 (Mon-Fri)

---

## Luồng Công Việc (Workflow)

```
┌─────────────────────────────────────────────────────────────┐
│                     START: Scheduler/Manual                 │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Extract Phase  │
                    └────────┬───────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    ┌─────────────────┐           ┌─────────────────┐
    │ VCB Scraper     │           │ TCB Scraper     │
    │ (API + XML)     │           │ (API JSON)      │
    └────────┬────────┘           └────────┬────────┘
             │                            │
             └────────────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Combine Raw Data    │
                    │ (VCB + TCB)         │
                    └────────┬────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Transform Phase      │
                  │ (cleaner.py)         │
                  └────────┬─────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐   ┌──────────────┐   ┌──────────┐
    │ Validate │   │ Standardize  │   │ Clean    │
    │ Data     │   │ Currency Code│   │ NA/Null  │
    └──────────┘   └──────────────┘   └──────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  ┌──────────────────────┐
                  │ Pandas DataFrame     │
                  │ (Final Clean Data)   │
                  └────────┬─────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │ Load Phase      │
                    │ (to PostgreSQL) │
                    └────────┬────────┘
                             │
          ┌──────────────────┴──────────────────┐
          ▼                                     ▼
    ┌─────────────┐                   ┌──────────────┐
    │ Record      │                   │ Record       │
    │ Exists?     │                   │ NOT Exists   │
    │ (Check UQ)  │                   │              │
    └──────┬──────┘                   └──────┬───────┘
           │                                 │
           ▼                                 ▼
    ┌─────────────┐                   ┌──────────────┐
    │ UPDATE      │                   │ INSERT NEW   │
    │ Old Record  │                   │ Record       │
    └──────┬──────┘                   └──────┬───────┘
           │                                 │
           └─────────────────┬────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Commit to DB    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Log Success     │
                    │ Exit Cleanly    │
                    └─────────────────┘
```

---

## Cấu Trúc Database

### Bảng 1: `dim_bank` (Dimension - Thông Tin Ngân Hàng)

| Cột | Kiểu Dữ Liệu | Khóa | Mô Tả |
|-----|--------------|------|-------|
| `bank_code` | VARCHAR(10) | ✅ PK | Mã ngân hàng (VCB, TCB, ...) |
| `bank_name` | VARCHAR(100) | | Tên ngân hàng |
| `bank_type` | VARCHAR(50) | | Loại ngân hàng (Commercial, ...) |

**Ví dụ dữ liệu:**
```
bank_code | bank_name      | bank_type
----------|----------------|----------
VCB       | Vietcombank    | Commercial
TCB       | Techcombank    | Commercial
```

### Bảng 2: `fact_exchange_rate` (Fact - Tỷ Giá)

| Cột | Kiểu Dữ Liệu | Khóa | Mô Tả |
|-----|--------------|------|-------|
| `id` | INTEGER | ✅ PK | Khóa chính (auto-increment) |
| `bank_code` | VARCHAR(10) | 🔗 FK | Tham chiếu tới dim_bank |
| `currency_code` | VARCHAR(20) | | Mã tiền tệ (USD, EUR, JPY, ...) |
| `currency_standard` | VARCHAR(3) | | Mã tiền chuẩn (USD, EUR, ...) |
| `buy_cash` | NUMERIC(15,2) | | Tỷ giá mua tiền mặt |
| `buy_transfer` | NUMERIC(15,2) | | Tỷ giá mua chuyển khoản |
| `sell` | NUMERIC(15,2) | | Tỷ giá bán |
| `record_date` | DATE | | Ngày ghi nhận dữ liệu |
| `created_at` | TIMESTAMP | | Thời gian tạo bản ghi (auto) |

**Unique Constraint:** `(bank_code, currency_code, record_date)`
- Đảm bảo không có bản ghi trùng lặp cho cùng ngân hàng, tiền tệ, ngày

**Ví dụ dữ liệu:**
```
id | bank_code | currency_code | currency_standard | buy_cash | buy_transfer | sell | record_date | created_at
---|-----------|---------------|-------------------|----------|--------------|------|-------------|---------------------
1  | VCB       | USD           | USD               | 24500    | 24520        | 24700| 2026-06-05  | 2026-06-05 08:30:00
2  | TCB       | USD           | USD               | 24510    | 24530        | 24690| 2026-06-05  | 2026-06-05 08:35:00
3  | VCB       | EUR           | EUR               | 26800    | 26820        | 27100| 2026-06-05  | 2026-06-05 08:32:00
```

---

## Chi Tiết Các Module
### 1. `main_etl.py` - Pipeline Chính
**Hàm chính:** `run_pipeline()`
**Công việc:**
1. Gọi VCB scraper để lấy dữ liệu
2. Gọi TCB scraper để lấy dữ liệu
3. Gộp dữ liệu từ cả 2 nguồn
4. Làm sạch dữ liệu bằng transformer
5. Nạp vào PostgreSQL sử dụng UPSERT logic:
   - Nếu bản ghi đã tồn tại → UPDATE giá trị mới
   - Nếu chưa tồn tại → INSERT bản ghi mới

**Hàm:** `load_to_postgresql(df)`
```python
for index, row in df.iterrows():
    existing_record = db.query(FactExchangeRate).filter(
        bank_code == row['bank_code'],
        currency_code == row['currency_code'],
        record_date == row['record_date']
    ).first()
    
    if existing_record:
        # UPDATE
        existing_record.buy_cash = row['buy_cash']
        # ... cập nhật các cột khác
    else:
        # INSERT
        new_record = FactExchangeRate(...)
        db.add(new_record)
    
    db.commit()
```

---
### 2. `scheduler.py` - Lên Lịch Tự Động

**Công nghệ:** APScheduler với CronTrigger
**Cấu hình:**
```python
scheduler.add_job(
    job_wrapper,
    CronTrigger(day_of_week='mon-fri', hour='9,18', minute='0'),
    id='banking_etl_job',
    name='Daily Banking ETL'
)
```

**Thời gian chạy:**
- 📅 **Thứ 2 - Thứ 6** (Mon-Fri)
- ⏰ **9:00 AM & 18:00 PM** (08:00 & 18:00)

**Chạy ngay lập tức (Debug):**
Bỏ comment dòng `job_wrapper()` trong file để test:
```python
# job_wrapper()  # Bỏ comment để test ngay
```

---

### 3. `extractors/vcb_scraper.py` - Scraper Vietcombank

**Nguồn dữ liệu:** Vietcombank API + XML fallback
**API chính:** `https://www.vietcombank.com.vn/api/exchangerates?date=YYYY-MM-DD`
**Hàm:** `extract_vcb_exchange_rate(date_obj)`
**Output:** List of dicts
```python
[
    {
        "bank_code": "VCB",
        "currency_code": "USD100",
        "currency_standard": "USD",
        "buy_cash": 2450000,
        "buy_transfer": 2452000,
        "sell": 2470000,
        "record_date": "2026-06-05"
    },
    ...
]
```
**Đặc điểm:**
- Hỗ trợ 2 API (mới & cũ)
- Validate ngày trả về khớp ngày request
- Xử lý retry và timeout
---
### 4. `extractors/tcb_scraper.py` - Scraper Techcombank
**Nguồn dữ liệu:** Techcombank API JSON
**API chính:** `https://techcombank.com/content/.../exchange-rates.integration.json`
**Hàm:** `extract_tcb_exchange_rate(date_obj)`
**Output:** Tương tự VCB
```python
[
    {
        "bank_code": "TCB",
        "currency_code": "USD",
        "buy_cash": 24510,
        "buy_transfer": 24530,
        "sell": 24690,
        "record_date": "2026-06-05"
    },
    ...
]
```
---
### 5. `transformers/cleaner.py` - Làm Sạch Dữ Liệu

**Hàm chính:** `clean_exchange_rate_data(vcb_raw_data, tcb_raw_data)`
**Công việc:**
1. Gộp dữ liệu từ VCB & TCB
2. Chuyển thành Pandas DataFrame
3. Chuẩn hóa mã tiền tệ
4. Xử lý giá trị NULL/NaN
5. Validate định dạng dữ liệu
6. Trả về DataFrame sạch

---
### 6. `db/database.py` - Quản Lý Database
**Công việc:**
- Khởi tạo kết nối PostgreSQL từ `DATABASE_URL`
- Tạo `SessionLocal` cho các module khác dùng
- Tạo `Base` class cho SQLAlchemy models

**Biến môi trường:**
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

---

### 7. `db/models.py` - SQLAlchemy Models
**Model 1: `DimBank`**
```python
class DimBank(Base):
    __tablename__ = 'dim_bank'
    bank_code = Column(String(10), primary_key=True)
    bank_name = Column(String(100))
    bank_type = Column(String(50))
```

**Model 2: `FactExchangeRate`**
```python
class FactExchangeRate(Base):
    __tablename__ = 'fact_exchange_rate'
    id = Column(Integer, primary_key=True)
    bank_code = Column(String(10))
    currency_code = Column(String(20))
    currency_standard = Column(String(3))
    buy_cash = Column(Numeric(15, 2))
    buy_transfer = Column(Numeric(15, 2))
    sell = Column(Numeric(15, 2))
    record_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('bank_code', 'currency_code', 'record_date', 
                        name='uq_exchange_rate'),
    )
```

---
## Testing & Debug
### Chạy Pipeline Thủ Công (Test)
```bash
# Kích hoạt môi trường
conda activate scraping (tôi đang dùng anaconda và bạn có thể cài hoặc cài môi trường ảo khác và chạy nhé)

# Chạy pipeline một lần
python main_etl.py
# Output mong đợi:
# [Extractor] Đang lấy dữ liệu từ VCB...
# [Extractor] Đang lấy dữ liệu từ TCB...
# [Transformer] Bắt đầu gộp và làm sạch dữ liệu...
# [Loader] Đang nạp XXX bản ghi vào cơ sở dữ liệu...
# [Loader] Hoàn thành!
```

### Kiểm Tra Dữ Liệu Trong Database

```sql
-- Xem các bản ghi tỷ giá mới nhất
SELECT * FROM fact_exchange_rate 
ORDER BY record_date DESC, created_at DESC 
LIMIT 20;

-- Xem thống kê theo ngân hàng
SELECT bank_code, currency_code, record_date, 
       COUNT(*) as count
FROM fact_exchange_rate
GROUP BY bank_code, currency_code, record_date
ORDER BY record_date DESC;

-- Tìm USD của VCB hôm nay
SELECT * FROM fact_exchange_rate
WHERE bank_code = 'VCB' 
  AND currency_code = 'USD'
  AND record_date = CURRENT_DATE;
```

### Khắc Phục Sự Cố Thường Gặp

| Lỗi | Nguyên Nhân | Giải Pháp |
|-----|-----------|----------|
| `DATABASE_URL not set` | Biến môi trường không được load | Kiểm tra file `.env`, chạy `load_dotenv()` |
| `Connection refused` | PostgreSQL chưa chạy | Khởi động PostgreSQL service |
| `UNIQUE constraint failed` | Dữ liệu trùng lặp | Check logic UPSERT trong `load_to_postgresql()` |
| `HTTP 403/404` | API website thay đổi | Update URL trong scraper hoặc dùng proxy |
| `Timeout error` | API chậm hoặc offline | Tăng timeout hoặc retry |

---

## Visualization (Tableau)
File `Book1.twb` là Tableau workbook chứa các dashboard:
- Tỷ giá theo thời gian
- So sánh giữa các ngân hàng
- Biến động tiền tệ

---
**Phiên bản:** 1.0
