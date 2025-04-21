# binance_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_binance_funding_rates():
    base_url = "https://fapi.binance.com"
    funding_url = f"{base_url}/fapi/v1/premiumIndex"
    tickers_url = f"{base_url}/fapi/v1/ticker/24hr"

    try:
        # Get volume data
        tickers_response = requests.get(tickers_url, timeout=10)
        volume_data = tickers_response.json()

        # Get funding rate data
        funding_response = requests.get(funding_url, timeout=10)
        funding_data = funding_response.json()

        # Build a volume map
        volume_map = {
            item["symbol"]: float(item["quoteVolume"])
            for item in volume_data
            if "symbol" in item and "quoteVolume" in item
        }

        results = []

        for item in funding_data:
            symbol = item.get("symbol", "")
            if not symbol:
                continue

            funding_rate = float(item.get("lastFundingRate", 0))
            volume_24h = volume_map.get(symbol, 0)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume_24h >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "Binance",
                    "symbol": symbol,
                    "funding_rate": funding_rate,
                    "volume_24h": volume_24h,
                    "contract_type": "PERPETUAL"
                })

            time.sleep(0.05)

        return results

    except Exception as e:
        print(f"[ERROR Binance] {e}")
        return []
