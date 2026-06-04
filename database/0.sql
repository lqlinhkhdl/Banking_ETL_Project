-- Xem toàn bộ 20 dòng dữ liệu tỷ giá sạch mà Python vừa nạp vào
SELECT 
    id,
    bank_code, 
    currency_code, 
    buy_cash, 
    buy_transfer, 
    sell, 
    record_date,
    created_at
FROM fact_exchange_rate
ORDER BY created_at DESC;