import requests
import time

def get_coinglass_funding_rates():
    url = "https://fapi.coinglass.com/api/fundingRate"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        print(f"[CoinGlass] Total activos recibidos: {len(data.get('data', {}))}")
        print(f"[CoinGlass DEBUG] Status code: {response.status_code}")
        print(f"[CoinGlass DEBUG] Raw response: {response.text[:500]}")  # imprimimos los primeros 500 caracteres


        result = []

        if "data" not in data:
            return []

        now = int(time.time() * 1000)

        for symbol, exchanges in data["data"].items():
            for exchange, funding_rate in exchanges.items():
                try:
                    # Normalizamos a formato compatible con el resto del bot
                    result.append({
                        "exchange": exchange,
                        "symbol": f"{symbol.upper()}USDT",
                        "funding_rate": float(funding_rate) / 100,  # CoinGlass da %
                        "volume_24h": 0,
                        "timestamp": now
                    })
                except Exception:
                    continue

        return result

    except Exception as e:
        print(f"[ERROR CoinGlass] {e}")
        return []
