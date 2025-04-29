# deribit_funding_bot.py (UPDATED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_deribit_funding_rates():
    instruments_url = "https://www.deribit.com/api/v2/public/get_instruments?currency=USDT&kind=future"
    try:
        instruments_response = requests.get(instruments_url, timeout=10)
        instruments_response.raise_for_status()
        instruments = instruments_response.json().get("result", [])
        print(f"[DERIBIT DEBUG] Instruments fetched: {len(instruments)}")
    except Exception as e:
        print(f"[DERIBIT ERROR] Failed to fetch instruments: {e}")
        return []

    results = []
    now_ms = int(time.time() * 1000)

    for instrument in instruments:
        try:
            symbol = instrument.get("instrument_name")
            if not symbol or not symbol.endswith("-PERPETUAL"):
                continue

            ticker_url = f"https://www.deribit.com/api/v2/public/ticker?instrument_name={symbol}"
            ticker_response = requests.get(ticker_url, timeout=10)
            if ticker_response.status_code != 200:
                continue

            ticker_data = ticker_response.json().get("result", {})

            funding_rate = ticker_data.get("funding_8h")
            volume = ticker_data.get("stats", {}).get("volume_usd")
            mark_price = ticker_data.get("mark_price")
            next_funding_ts = ticker_data.get("next_funding_time")
            open_interest = ticker_data.get("open_interest")

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
            print(f"[DERIBIT WARNING] Error parsing {symbol}: {e}")
            continue

    print(f"[Deribit] Filtered pairs: {len(results)}")
    return results
