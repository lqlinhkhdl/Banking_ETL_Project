-- 1. Bảng Thông tin Ngân hàng
CREATE TABLE dim_bank (
    bank_code VARCHAR(10) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    bank_type VARCHAR(50)
);

-- 2. Bảng Lịch sử Tỷ giá Ngoại tệ
CREATE TABLE fact_exchange_rate (
    id SERIAL PRIMARY KEY,
    bank_code VARCHAR(10) REFERENCES dim_bank(bank_code),
    currency_code VARCHAR(3) NOT NULL,
    buy_cash NUMERIC(15, 2),
    buy_transfer NUMERIC(15, 2),
    sell NUMERIC(15, 2),
    record_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_exchange_rate UNIQUE (bank_code, currency_code, record_date)
);

-- 3. Bảng Lịch sử Lãi suất Tiền gửi
CREATE TABLE fact_interest_rate (
    id SERIAL PRIMARY KEY,
    bank_code VARCHAR(10) REFERENCES dim_bank(bank_code),
    term_months INT NOT NULL,
    interest_rate NUMERIC(5, 2) NOT NULL,
    record_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_interest_rate UNIQUE (bank_code, term_months, record_date)
);

-- 4. Bảng Lịch sử Giao dịch Chứng khoán
CREATE TABLE fact_stock_price (
    id SERIAL PRIMARY KEY,
    bank_code VARCHAR(10) REFERENCES dim_bank(bank_code),
    close_price NUMERIC(15, 2) NOT NULL,
    volume BIGINT NOT NULL,
    record_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_stock_price UNIQUE (bank_code, record_date)
);

-- Nạp sẵn dữ liệu Dimension cơ sở
INSERT INTO dim_bank (bank_code, bank_name, bank_type) VALUES
('VCB', 'Ngan hang TMCP Ngoai thuong Viet Nam', 'NHTM Nha nuoc'),
('TCB', 'Ngan hang TMCP Ky thuong Viet Nam', 'NHTM Co phan'),
('MBB', 'Ngan hang TMCP Quan doi', 'NHTM Nha nuoc'),
('VPB', 'Ngan hang TMCP Viet Nam Thinh Vuong', 'NHTM Co phan'),
('ACB', 'Ngan hang TMCP A Chau', 'NHTM Co phan')
ON CONFLICT (bank_code) DO NOTHING;