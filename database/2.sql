-- 1. Nới rộng cột cũ từ VARCHAR(3) thành VARCHAR(20)
ALTER TABLE fact_exchange_rate 
ALTER COLUMN currency_code TYPE VARCHAR(20);

-- 2. Thêm một cột mới để lưu mã tiền chuẩn (ví dụ: USD, EUR) phục vụ Tableau
ALTER TABLE fact_exchange_rate 
ADD COLUMN currency_standard VARCHAR(3);

-- 3. Xóa bỏ ràng buộc UNIQUE cũ (vì bộ ba khóa ngoại cũ có VARCHAR(3))
ALTER TABLE fact_exchange_rate 
DROP CONSTRAINT IF EXISTS uq_exchange_rate;

-- 4. Tạo lại ràng buộc UNIQUE mới bao gồm cả cột chi tiết và cột chuẩn
ALTER TABLE fact_exchange_rate 
ADD CONSTRAINT uq_exchange_rate UNIQUE (bank_code, currency_code, record_date);