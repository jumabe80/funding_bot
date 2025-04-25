# kucoin_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_kucoin_funding_rates():
    url_base = "https://api-futures.kucoin.com"

    try:
        market_response = requests.get(f"{url_base}/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])
    except Exception as e:
        print(f"[ERROR KuCoin] Failed to fetch contracts: {e}")
        return []

    results = []
    for contract in contracts:
        symbol = contract.get("symbol")
        if not symbol:
            continue

        try:
            ticker_resp = requests.get(f"{url_base}/api/v1/contract/market/ticker?symbol={symbol}", timeout=10)
            ticker_data = ticker_resp.json().get("data", {})
            quote_volume = float(ticker_data.get("turnoverOf24h", 0))
        except Exception as e:
            print(f"[ERROR KuCoin] Ticker issue for {symbol}: {e}")
            continue

        if quote_volume < VOLUME_24H_THRESHOLD:
            continue

        try:
            funding_resp = requests.get(f"{url_base}/api/v1/funding-rate/{symbol}", timeout=10)
            funding_data = funding_resp.json().get("data", {})
            funding_rate_str = funding_data.get("value")
            if funding_rate_str in [None, ""]:
                continue
            funding_rate = float(funding_rate_str)
        except Exception as e:
            print(f"[ERROR KuCoin] Funding rate issue for {symbol}: {e}")
            continue

        if funding_rate >= FUNDING_RATE_THRESHOLD:
            results.append({
                "exchange": "KuCoin",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": quote_volume,
                "contract_type": "PERPETUAL",  # Assuming KuCoin only offers perpetuals on this endpoint
                "funding_time_min": 480  # KuCoin funds every 8 hours
            })

        time.sleep(0.1)

    print(f"[KuCoin] Filtered pairs: {len(results)}")
    return results
