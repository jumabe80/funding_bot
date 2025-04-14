import requests

def get_binance_funding_rates():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    response = requests.get(url)
    data = response.json()

    results = []
    for item in data:
        if item.get("symbol", "").endswith("USDT") and item.get("lastFundingRate") is not None:
            funding_rate = float(item["lastFundingRate"])
            mark_price = float(item.get("markPrice", 0))
            volume_estimate = mark_price * 1000000  # Estimación ficticia del volumen

            results.append({
                "exchange": "Binance",
                "symbol": item["symbol"],
                "funding_rate": funding_rate,
                "volume_24h": volume_estimate,
                "timestamp": int(item["time"])
            })
    return results
