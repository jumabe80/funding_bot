# kucoin_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_kucoin_funding_rates():
    base_url = "https://api.kucoin.com"
    results = []

    try:
        # Step 1: Get all perpetual contracts
        market_response = requests.get(f"{base_url}/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        for contract in contracts:
            symbol = contract.get("symbol")
            if not symbol:
                continue

            # Step 2: Get ticker for volume
            ticker_resp = requests.get(f"{base_url}/api/v1/contract/market/ticker?symbol={symbol}", timeout=10)
            ticker_data = ticker_resp.json().get("data", {})

            quote_volume = float(ticker_data.get("turnoverOf24h", 0))
            if quote_volume < VOLUME_24H_THRESHOLD:
                continue

            # Step 3: Get funding rate
            funding_resp = requests.get(f"{base_url}/api/v1/funding-rate/{symbol}", timeout=10)
            funding_data = funding_resp.json().get("data", {})

            funding_rate_str = funding_data.get("value")
            if funding_rate_str in [None, ""]:
                continue

            try:
                funding_rate = float(funding_rate_str)
            except ValueError:
                continue

            if funding_rate < FUNDING_RATE_THRESHOLD:
                continue

            # Step 4: Calculate funding countdown (every 8h)
            now_ts = int(time.time())
            funding_interval_sec = 8 * 60 * 60
            time_since_last = now_ts % funding_interval_sec
            countdown_min = (funding_interval_sec - time_since_last) // 60

            results.append({
                "exchange": "KuCoin",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": quote_volume,
                "contract_type": "PERPETUAL",
                "funding_countdown": countdown_min
            })

            time.sleep(0.1)

        return results

    except Exception as e:
        print(f"[ERROR KuCoin] {e}")
        return []
