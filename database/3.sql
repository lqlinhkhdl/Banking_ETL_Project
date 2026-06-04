CREATE OR REPLACE VIEW v_tableau_exchange_rate AS
SELECT 
    bank_code,
    currency_standard AS currency_code, -- Đổi tên thành mã chuẩn (USD, EUR...)
    -- Lấy giá trị lớn nhất trong ngày để đại diện cho tỷ giá chuẩn của ngân hàng đó
    MAX(buy_cash) AS buy_cash,
    MAX(buy_transfer) AS buy_transfer,
    MAX(sell) AS sell,
    record_date
FROM fact_exchange_rate
WHERE sell > 0 -- Loại bỏ các dòng lỗi hoặc không có giá bán
GROUP BY bank_code, currency_standard, record_date;