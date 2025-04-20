# bybit_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_bybit_funding_rates():
    base_url = "https://api.bybit.com"
    tickers_url = f"{base_url}/v5/market/tickers?category=linear"
    funding_url = f"{base_url}/v5/market/funding/prev-funding-rate"

    try:
        tickers_response = requests.get(tickers_url, timeout=10)
        tickers_data = tickers_response.json().get("result", {}).get("list", [])
        now = int(time.time() * 1000)
        results = []

        for ticker in tickers_data:
            symbol = ticker.get("symbol")
            quote_volume = float(ticker.get("turnover24h", 0))

            if quote_volume < VOLUME_24H_THRESHOLD:
                continue

            funding_resp = requests.get(f"{funding_url}?symbol={symbol}", timeout=10)
            if funding_resp.status_code != 200:
                continue

            funding_data = funding_resp.json().get("result", {})
            if not funding_data:
                continue

            funding_rate = float(funding_data.get("fundingRate", 0))

            if funding_rate >= FUNDING_RATE_THRESHOLD:
                results.append({
                    "exchange": "Bybit",
                    "symbol": symbol,
                    "funding_rate": funding_rate,
                    "volume_24h": quote_volume,
                    "timestamp": now,
                    "contract_type": "PERPETUAL"
                })

            time.sleep(0.25)  # To respect rate limits

        return results

    except Exception as e:
        print(f"[ERROR Bybit] {e}")
        return []
