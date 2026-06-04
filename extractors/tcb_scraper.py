from __future__ import annotations
import requests
import time
from datetime import datetime, timedelta

BASE = (
    "https://techcombank.com/content/techcombank/web/vn/vi"
    "/cong-cu-tien-ich/ty-gia/_jcr_content"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://techcombank.com/cong-cu-tien-ich/ty-gia",
}


def _build_url(date: datetime) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    d = date.strftime("%Y-%m-%d")
    if d == today:
        return f"{BASE}.exchange-rates.integration.json"
    return f"{BASE}.exchange-rates.{d}.integration.json"


def _parse(data: dict, date_str: str) -> list[dict]:
    records = []
    for item in data.get("exchangeRate", {}).get("data", []):
        records.append({
            "bank_code":     "TCB",
            "currency_code": item["label"],
            "buy_cash":      item.get("bidRateTM", ""),
            "buy_transfer":  item.get("bidRateCK", ""),
            "sell":          item.get("askRate",   ""),
            "record_date":   date_str,
        })
    return records


def detect_history_limit() -> int:
    """
    Tự động tìm giới hạn lịch sử TCB lưu trữ.
    Thử các mốc 7, 14, 30, 60, 90 ngày — trả về số ngày xa nhất còn data.
    """
    print("[TCB] Đang kiểm tra giới hạn lịch sử...")
    checkpoints = [7, 14, 30, 60, 90]
    limit = 0
    for days_ago in checkpoints:
        date = datetime.now() - timedelta(days=days_ago)
        d = date.strftime("%Y-%m-%d")
        url = f"{BASE}.exchange-rates.{d}.integration.json"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            status = r.status_code
            has_data = bool(r.json().get("exchangeRate", {}).get("data")) if status == 200 else False
            print(f"  {d} ({days_ago:>2} ngày trước): HTTP {status} {'✓' if has_data else '✗'}")
            if has_data:
                limit = days_ago
        except Exception as e:
            print(f"  {d} ({days_ago:>2} ngày trước): lỗi — {e}")
        time.sleep(0.3)
    print(f"[TCB] Lịch sử tối đa khả dụng: ~{limit} ngày\n")
    return limit


def extract_tcb_exchange_rate(days_back: int = 30, delay: float = 0.5) -> list[dict]:
    """
    Lấy tỷ giá Techcombank cho n ngày gần nhất trực tiếp từ API JSON của TCB.

    Args:
        days_back: số ngày muốn lấy (mặc định 30)
        delay:     thời gian nghỉ giữa các request (giây, mặc định 0.5)

    Returns:
        list các dict với keys: bank_code, currency_code,
                                buy_cash, buy_transfer, sell, record_date
    """
    raw_data = []
    skipped = 0
    print(f"[TCB] Bắt đầu lấy dữ liệu {days_back} ngày qua...")

    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        url = _build_url(date)

        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)

            if resp.status_code == 404:
                print(f"  -> {date_str}: không có dữ liệu (cuối tuần / lễ)")
                skipped += 1
                continue

            resp.raise_for_status()
            records = _parse(resp.json(), date_str)

            if records:
                raw_data.extend(records)
                print(f"  -> {date_str}: {len(records):>2} mã tiền ✓")
            else:
                print(f"  -> {date_str}: response rỗng")
                skipped += 1

        except requests.exceptions.Timeout:
            print(f"  -> {date_str}: timeout, bỏ qua")
            skipped += 1
        except requests.exceptions.HTTPError as e:
            print(f"  -> {date_str}: HTTP error — {e}")
            skipped += 1
        except Exception as e:
            print(f"  -> {date_str}: lỗi — {e}")
            skipped += 1

        if i < days_back - 1:
            time.sleep(delay)

    days_with_data = (days_back - skipped)
    print(f"\n[TCB] Hoàn thành.")
    print(f"      Ngày có data : {days_with_data} / {days_back}")
    print(f"      Ngày bỏ qua  : {skipped} (cuối tuần / lễ / lỗi)")
    print(f"      Tổng bản ghi : {len(raw_data)}")
    return raw_data


if __name__ == "__main__":
    # Bước 1 (tuỳ chọn): kiểm tra TCB lưu lịch sử bao nhiêu ngày
    limit = detect_history_limit()

    # Bước 2: lấy dữ liệu — dùng limit tìm được, hoặc tự đặt số ngày
    days = min(limit, 30) if limit else 30
    data = extract_tcb_exchange_rate(days_back=days, delay=0.5)

    # Bước 3: xem thử kết quả
    if data:
        print(f"\n--- 5 bản ghi đầu tiên ---")
        for row in data[:5]:
            print(row)