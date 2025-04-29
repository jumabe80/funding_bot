# bitget_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_bitget_funding_rates():
    base_url = "https://api.bitget.com"
    try:
        # Step 1: Get all USDT perpetual tickers
        tickers_url = f"{base_url}/api/v2/mix/market/tickers?productType=usdt-futures"
        tickers_response = requests.get(tickers_url, timeout=10)
        tickers = tickers_response.json().get("data", [])

        results = []

        for ticker in tickers:
            symbol = ticker.get("symbol")
            funding_rate_str = ticker.get("fundingRate")
            volume_str = ticker.get("quoteVolume")
            
            if not symbol or funding_rate_str in [None, ""] or volume_str in [None, ""]:
                continue

            try:
                funding_rate = float(funding_rate_str)
                volume_24h = float(volume_str)
            except ValueError:
                continue

            if funding_rate < FUNDING_RATE_THRESHOLD:
                continue

            if volume_24h < VOLUME_24H_THRESHOLD:
                continue

            # Step 2: Funding countdown estimation (Bitget funds every 8 hours)
            now_ts = int(time.time())
            funding_interval_sec = 8 * 60 * 60
            time_since_last = now_ts % funding_interval_sec
            countdown_min = (funding_interval_sec - time_since_last) // 60

            results.append({
                "exchange": "Bitget",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": int(volume_24h),
                "contract_type": "PERPETUAL",
                "funding_countdown": countdown_min
            })
            
            time.sleep(0.1)  # Respect rate limits

        return results

    except Exception as e:
        print(f"[ERROR Bitget] {e}")
        return []
