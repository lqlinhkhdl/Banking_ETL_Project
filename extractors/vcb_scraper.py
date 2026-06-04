from __future__ import annotations
import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

NEW_API = "https://www.vietcombank.com.vn/api/exchangerates"
OLD_API = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.vietcombank.com.vn/ty-gia",
}


def _fetch_new_api(date: datetime) -> list[dict]:
    date_str = date.strftime("%Y-%m-%d")
    resp = requests.get(NEW_API, params={"date": date_str}, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    payload = resp.json()

    # Kiểm tra ngày trả về có khớp ngày request không
    returned_date = payload.get("Date", "")[:10]  # "2026-06-03T00:00:00" -> "2026-06-03"
    if returned_date and returned_date != date_str:
        raise ValueError(f"Date mismatch: request={date_str}, response={returned_date}")

    items = payload.get("Data", [])
    records = []
    for item in items:
        records.append({
            "bank_code":     "VCB",
            "currency_code": item["currencyCode"],
            "buy_cash":      item.get("cash",     ""),
            "buy_transfer":  item.get("transfer", ""),
            "sell":          item.get("sell",     ""),
            "record_date":   date_str,
        })
    return records


def _fetch_old_xml(date: datetime) -> list[dict]:
    """
    API cũ (fallback): XML, tham số date=DD/MM/YYYY
    """
    date_param = date.strftime("%d/%m/%Y")
    date_str   = date.strftime("%Y-%m-%d")

    resp = requests.get(OLD_API, params={"date": date_param}, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    records = []
    for exrate in root.findall("Exrate"):
        records.append({
            "bank_code":     "VCB",
            "currency_code": exrate.get("CurrencyCode", ""),
            "buy_cash":      exrate.get("Buy",          ""),
            "buy_transfer":  exrate.get("Transfer",     ""),
            "sell":          exrate.get("Sell",         ""),
            "record_date":   date_str,
        })
    return records


def extract_vcb_exchange_rate(days_back: int = 30, delay: float = 0.5) -> list[dict]:
    """
    Lấy tỷ giá Vietcombank cho n ngày gần nhất.
    Ưu tiên API JSON mới — fallback sang XML cũ nếu lỗi.
    """
    raw_data = []
    skipped  = 0
    print(f"[VCB] Bắt đầu lấy dữ liệu {days_back} ngày qua...")

    for i in range(days_back):
        date     = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        records  = []

        # Thử API JSON mới trước
        try:
            records = _fetch_new_api(date)
            source  = "JSON API mới"
        except Exception as e_new:
            print(f"  -> {date_str}: JSON API lỗi ({e_new}) — thử XML cũ...")
            # Fallback sang XML cũ
            try:
                records = _fetch_old_xml(date)
                source  = "XML API cũ"
            except Exception as e_old:
                print(f"  -> {date_str}: XML API cũng lỗi ({e_old}) — bỏ qua")
                skipped += 1
                continue

        if records:
            raw_data.extend(records)
            print(f"  -> {date_str}: {len(records):>2} mã tiền ✓  [{source}]")
        else:
            print(f"  -> {date_str}: không có dữ liệu (cuối tuần / lễ)")
            skipped += 1

        if i < days_back - 1:
            time.sleep(delay)

    days_with_data = days_back - skipped
    print(f"\n[VCB] Hoàn thành.")
    print(f"      Ngày có data : {days_with_data} / {days_back}")
    print(f"      Ngày bỏ qua  : {skipped} (cuối tuần / lễ / lỗi)")
    print(f"      Tổng bản ghi : {len(raw_data)}")
    return raw_data


if __name__ == "__main__":
    data = extract_vcb_exchange_rate(days_back=30, delay=0.5)
    if data:
        print(f"\n--- 5 bản ghi đầu tiên ---")
        for row in data[:5]:
            print(row)