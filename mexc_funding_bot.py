# mexc_funding_bot.py (UPDATED - FUNDING RATE FIXED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

TICKERS_URL = "https://contract.mexc.com/api/v1/contract/ticker"
FUNDING_RATE_URL = "https://futures.mexc.com/api/v1/contract/funding_rate/{symbol}"

def get_mexc_funding_rates():
    results = []
    now_sec = int(time.time())

    try:
        ticker_response = requests.get(TICKERS_URL, timeout=15)
        ticker_response.raise_for_status()
        ticker_data = ticker_response.json().get("data", [])
        print(f"[MEXC] Contracts fetched: {len(ticker_data)}")
    except Exception as e:
        print(f"[MEXC ERROR] Failed to fetch tickers: {e}")
        return []

    for ticker in ticker_data:
        try:
            symbol = ticker.get("symbol")
            if not symbol or not symbol.endswith("_USDT"):
                continue

            volume = float(ticker.get("amount24", 0))
            mark_price = float(ticker.get("lastPrice", 0))
            open_interest = float(ticker.get("holdVol", 0))
            volume_usdt = volume * mark_price

            # ✅ NEW: Fetch real funding rate
            funding_resp = requests.get(FUNDING_RATE_URL.format(symbol=symbol), timeout=10)
            funding_resp.raise_for_status()
            funding_data = funding_resp.json().get("data", {})
            funding_rate = float(funding_data.get("fundingRate", 0))
            next_funding_time = int(funding_data.get("nextSettleTime", 0)) // 1000
            funding_countdown = max(0, next_funding_time - now_sec)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume_usdt >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "MEXC",
                    "symbol": symbol.replace("_USDT", "-USDT-PERP"),
                    "funding_rate": funding_rate,
                    "volume_24h": int(volume_usdt),
                    "timestamp": now_sec,
                    "contract_type": "PERPETUAL",
                    "funding_countdown": funding_countdown
                })

        except Exception as e:
            print(f"[MEXC WARNING] Error processing {symbol}: {e}")
            continue

    print(f"[MEXC] Filtered pairs: {len(results)}")
    return results
