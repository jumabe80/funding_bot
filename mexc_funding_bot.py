# mexc_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD


def get_mexc_funding_rates():
    url = "https://contract.mexc.com/api/v1/contract/detail"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        contracts = response.json().get("data", [])
        print(f"[MEXC] Contracts fetched: {len(contracts)}")
    except Exception as e:
        print(f"[MEXC ERROR] Failed to fetch contracts: {e}")
        return []

    results = []
    now_sec = int(time.time())

    for contract in contracts:
        try:
            symbol = contract.get("symbol")
            if not symbol or "USDT" not in symbol:
                continue

            funding_rate = contract.get("fundingRate")
            volume_base = contract.get("volume")
            mark_price = contract.get("lastPrice")
            next_funding_ts = contract.get("fundingTime")  # Usually in ms

            if None in (funding_rate, volume_base, mark_price, next_funding_ts):
                continue

            try:
                funding_rate = float(funding_rate)
                volume_base = float(volume_base)
                mark_price = float(mark_price)
                next_funding_ts = int(next_funding_ts / 1000)  # Convert ms to seconds
            except:
                continue

            volume_usdt = volume_base * mark_price
            time_to_funding_min = abs(int((next_funding_ts - now_sec) / 60))

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume_usdt >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "MEXC",
                    "symbol": symbol,
                    "funding_rate": funding_rate,
                    "volume_24h": round(volume_usdt),
                    "timestamp": now_sec,
                    "contract_type": "PERPETUAL",
                    "funding_countdown": time_to_funding_min
                })
        except Exception as e:
            print(f"[MEXC WARNING] Error parsing contract {symbol}: {e}")
            continue

    print(f"[MEXC] Filtered pairs: {len(results)}")
    return results
