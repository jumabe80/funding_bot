import requests
import time

def get_binance_funding_rates():
    url_funding = "https://fapi.binance.com/fapi/v1/premiumIndex"
    url_volume = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    url_info = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    try:
        funding_data = requests.get(url_funding, timeout=10).json()
        volume_data = requests.get(url_volume, timeout=10).json()
        info_data = requests.get(url_info, timeout=10).json()

        volume_map = {
            item["symbol"]: float(item.get("quoteVolume", 0))
            for item in volume_data if item.get("quoteVolume") is not None
        }

        contract_type_map = {
            item["symbol"]: item.get("contractType", "")
            for item in info_data.get("symbols", [])
        }

        now = int(time.time() * 1000)
        result = []

        for item in funding_data:
            symbol = item.get("symbol", "")
            if item.get("lastFundingRate") is not None:
                funding_rate = float(item["lastFundingRate"])
                volume_24h = volume_map.get(symbol, 0.0)
                contract_type = contract_type_map.get(symbol, "")

                result.append({
                    "exchange": "Binance",
                    "symbol": symbol,
                    "funding_rate": funding_rate,
                    "volume_24h": volume_24h,
                    "timestamp": int(item["time"]),
                    "contract_type": contract_type
                })

        return result

    except Exception as e:
        print(f"[ERROR Binance] {e}")
        return []
