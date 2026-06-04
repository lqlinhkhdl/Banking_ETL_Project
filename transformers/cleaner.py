import pandas as pd
import numpy as np

def clean_exchange_rate_data(vcb_raw_data, tcb_raw_data):
    """
    Gộp và làm sạch dữ liệu từ nhiều nguồn ngân hàng.
    Trả về một Pandas DataFrame đã chuẩn hóa 100%, bổ sung cột mã tiền chuẩn.
    """
    print("[Transformer] Bắt đầu gộp và làm sạch dữ liệu...")
    
    # 1. Gộp 2 list dữ liệu lại với nhau
    combined_raw_data = vcb_raw_data + tcb_raw_data
    
    # 2. Chuyển đổi thành Pandas DataFrame
    df = pd.DataFrame(combined_raw_data)
    
    if df.empty:
        print("[Transformer] Cảnh báo: Không có dữ liệu đầu vào!")
        return df

    # 3. Danh sách các cột chứa giá trị tiền tệ cần làm sạch
    price_columns = ['buy_cash', 'buy_transfer', 'sell']
    
    for col in price_columns:
        # Ép kiểu toàn bộ về chuỗi (string) để dễ xử lý, lấp đầy giá trị rỗng bằng chuỗi trống
        df[col] = df[col].astype(str).fillna('')
        
        # Dùng Regex gộp để loại bỏ mọi ký tự rác (dấu phẩy, khoảng trắng, chữ VND, ký hiệu ₫)
        df[col] = df[col].str.replace(r'[,\sVND₫]', '', regex=True)
        
        # Chuyển đổi những chuỗi chỉ có gạch ngang '-' hoặc rỗng thành NaN (Not a Number)
        df[col] = df[col].replace(['-', ''], np.nan)
        
        # Ép kiểu về dạng số thực (float). 
        # errors='coerce' đảm bảo nếu còn sót ký tự lạ nào không thể ép kiểu, nó sẽ tự biến thành NaN thay vì báo lỗi sập luồng.
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Làm sạch cột mã tiền tệ (Currency Code) & TẠO CỘT CHUẨN MỚI
    # Loại bỏ khoảng trắng thừa và viết hoa toàn bộ (VD: ' usd ' -> 'USD')
    df['currency_code'] = df['currency_code'].astype(str).str.strip().str.upper()

    # --- BỔ SUNG LOGIC CÁCH 2 Ở ĐÂY ---
    # Tạo cột phụ currency_standard: Chỉ cắt lấy đúng 3 ký tự đầu tiên để Tableau dùng vẽ biểu đồ (Ví dụ: "USD (50-100)" -> "USD")
    df['currency_standard'] = df['currency_code'].str.slice(0, 3)
    # ----------------------------------

    # 5. Loại bỏ các dòng rác (Những dòng không có mã tiền tệ hợp lệ)
    df = df[df['currency_code'] != '']
    df = df[df['currency_code'] != 'NAN']
    # Giữ nguyên logic xử lý giá trị khuyết thiếu bằng số 0 cho cột tiền mặt của bạn
    df['buy_cash'] = df['buy_cash'].fillna(0)
    df['buy_transfer'] = df['buy_transfer'].fillna(0)
    df['sell'] = df['sell'].fillna(0)                 # <-- THÊM DÒNG NÀY ĐỂ FIX LỖI
    # 6. Ép kiểu cột record_date về định dạng Date chuẩn
    df['record_date'] = pd.to_datetime(df['record_date']).dt.date

    # In ra báo cáo tóm tắt
    print(f"[Transformer] Đã làm sạch thành công {len(df)} dòng dữ liệu.")
    
    # Trả về DataFrame sạch đẹp chứa cả 2 cột mã tiền
    return df