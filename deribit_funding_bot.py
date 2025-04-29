# deribit_funding_bot.py (DEBUG MODE ENABLED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_deribit_funding_rates():
    url = "https://www.deribit.com/api/v2/public/get_instruments?currency=USDT&kind=future"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        contracts = response.json().get("result", [])
        print(f"[DERIBIT DEBUG] Contracts fetched: {len(contracts)}")
    except Exception as e:
        print(f"[DERIBIT ERROR] Failed to fetch contracts: {e}")
        return []

    results = []
    now_ms = int(time.time() * 1000)

    for contract in contracts:
        try:
            symbol = contract.get("instrument_name")
            if not symbol or "PERPETUAL" not in symbol:
                continue

            funding_rate = contract.get("funding_rate")
            volume = contract.get("volume_usdt_24h")
            mark_price = contract.get("mark_price")
            next_funding_ts = contract.get("next_funding_time")
            open_interest = contract.get("open_interest")

            if None in (funding_rate, volume, mark_price, next_funding_ts):
                continue

            try:
                funding_rate = float(funding_rate)
                volume = float(volume)
                mark_price = float(mark_price)
                next_funding_ts = int(next_funding_ts)
                open_interest = float(open_interest)
            except:
                continue

            time_to_funding_min = int((next_funding_ts - now_ms) / 60000)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "Deribit",
                    "symbol": symbol,
                    "funding_rate": funding_rate,
                    "volume_24h": round(volume),
                    "timestamp": now_ms,
                    "contract_type": "PERPETUAL",
                    "funding_countdown": time_to_funding_min
                })
        except Exception as e:
            print(f"[DERIBIT WARNING] Error parsing contract {symbol}: {e}")
            continue

    print(f"[Deribit] Filtered pairs: {len(results)}")
    return results
