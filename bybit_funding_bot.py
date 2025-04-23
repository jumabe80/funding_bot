# bybit_funding_bot.py (UPDATED WITH CORRECT FUNDING & VOLUME PARSING)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_bybit_funding_rates():
    try:
        tickers_response = requests.get("https://api.bybit.com/v5/market/tickers?category=linear", timeout=10)
        tickers_data = tickers_response.json().get("result", {}).get("list", [])
    except Exception as e:
        print(f"[ERROR Bybit] Failed to fetch tickers: {e}")
        return []

    results = []

    for ticker in tickers_data:
        symbol = ticker.get("symbol")
        turnover_raw = ticker.get("turnover24h", 0)
        funding_rate_raw = ticker.get("fundingRate")

        try:
            turnover = float(turnover_raw)
        except ValueError:
            turnover = 0

        if not funding_rate_raw:
            continue

        try:
            funding_rate = float(funding_rate_raw)
        except ValueError:
            continue

        if turnover >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
            results.append({
                "exchange": "Bybit",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": turnover,
                "contract_type": "PERPETUAL"
            })

        time.sleep(0.25)

    print(f"[Bybit] Pares filtrados: {len(results)}")
    return results
