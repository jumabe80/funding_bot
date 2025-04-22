# bybit_funding_bot.py (UPDATED with contract_type)
import requests

from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_bybit_funding_rates():
    url = "https://api.bybit.com/v5/market/tickers?category=linear"
    response = requests.get(url, timeout=10)
    data = response.json()

    funding_data = data.get("result", {}).get("list", [])

    results = []

    for item in funding_data:
        symbol = item.get("symbol", "")
        funding_rate_raw = item.get("fundingRate")
        if not funding_rate_raw:
            continue  # Skip if fundingRate is missing or empty
        funding_rate = float(funding_rate_raw)
        volume_24h = float(item.get("turnover24h", 0))

        if funding_rate >= FUNDING_RATE_THRESHOLD and volume_24h >= VOLUME_24H_THRESHOLD:
            results.append({
                "exchange": "Bybit",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": volume_24h,
                "timestamp": None,  # Bybit doesn't send timestamp easily
                "contract_type": "PERPETUAL"  # Added for consistency
            })

    return results

if __name__ == "__main__":
    rates = get_bybit_funding_rates()
    for r in rates:
        print(r)
