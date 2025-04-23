# binance_funding_bot.py (UPDATED TO INCLUDE FUNDING COUNTDOWN)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_binance_funding_rates():
    try:
        funding_response = requests.get("https://fapi.binance.com/fapi/v1/premiumIndex", timeout=10)
        funding_data = funding_response.json()

        volume_response = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=10)
        volume_data = volume_response.json()
    except Exception as e:
        print(f"[ERROR Binance] Failed to fetch data: {e}")
        return []

    volume_map = {
        item["symbol"]: float(item["quoteVolume"])
        for item in volume_data
        if "quoteVolume" in item and item["quoteVolume"] is not None
    }

    results = []

    for item in funding_data:
        symbol = item.get("symbol", "")
        if item.get("lastFundingRate") is None:
            continue

        try:
            funding_rate = float(item["lastFundingRate"])
        except ValueError:
            continue

        volume_24h = volume_map.get(symbol, 0)

        # Compute funding countdown from nextFundingTime
        try:
            next_ts = int(item.get("nextFundingTime", 0))
            now_ts = int(time.time() * 1000)
            minutes_until = max((next_ts - now_ts) // 60000, 0)
        except:
            minutes_until = None

        if funding_rate >= FUNDING_RATE_THRESHOLD and volume_24h >= VOLUME_24H_THRESHOLD:
            results.append({
                "exchange": "Binance",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": volume_24h,
                "contract_type": "PERPETUAL",
                "funding_countdown": minutes_until
            })

    print(f"[Binance] Filtered pairs: {len(results)}")
    return results
