import requests

def get_binance_funding_rates():
    # Obtener funding rates
    funding_url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    funding_response = requests.get(funding_url)
    funding_data = funding_response.json()

    # Obtener volumen 24h
    volume_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    volume_response = requests.get(volume_url)
    volume_data = volume_response.json()

    # Crear diccionario {"BTCUSDT": volumen_24h_en_USDT}
    volume_map = {
        item["symbol"]: float(item["quoteVolume"])
        for item in volume_data
        if item["symbol"].endswith("USDT")
    }

    results = []
    for item in funding_data:
        symbol = item.get("symbol", "")
        if symbol.endswith("USDT") and item.get("lastFundingRate") is not None:
            funding_rate = float(item["lastFundingRate"])
            volume_24h = volume_map.get(symbol, 0)

            results.append({
                "exchange": "Binance",
                "symbol": symbol,
                "funding_rate": funding_rate,
                "volume_24h": volume_24h,
                "timestamp": int(item["time"])
            })

    return results
