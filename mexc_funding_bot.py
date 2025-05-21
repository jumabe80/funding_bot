# mexc_funding_bot.py (FIXED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

FUNDING_RATE_URL = "https://contract.mexc.com/api/v1/position/fundingRate?symbol={symbol}"
TICKERS_URL = "https://contract.mexc.com/api/v1/contract/ticker"


def get_mexc_funding_rates():
    results = []
    now_sec = int(time.time())

    try:
        ticker_response = requests.get(TICKERS_URL, timeout=10)
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

            volume = float(ticker.get("amount24"))
            mark_price = float(ticker.get("lastPrice"))
            open_interest = float(ticker.get("holdVol"))

            time.sleep(0.3)  # prevent rate-limiting

            try:
                funding_resp = requests.get(FUNDING_RATE_URL.format(symbol=symbol), timeout=10)
                funding_resp.raise_for_status()
                funding_data = funding_resp.json().get("data", {})
                funding_rate = float(funding_data.get("fundingRate", 0))
                next_funding_time = int(funding_data.get("nextSettleTime", 0)) // 1000
            except Exception as f_err:
                print(f"[MEXC WARNING] No funding data for {symbol}, skipping. Error: {f_err}")
                continue

            volume_usdt = volume * mark_price
            time_to_funding_min = int((next_funding_time - now_sec) / 60)
            time_to_funding_min = max(0, time_to_funding_min)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume_usdt >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "MEXC",
                    "symbol": symbol.replace("_USDT", "-USDT-PERP"),
                    "funding_rate": funding_rate,
                    "volume_24h": int(volume_usdt),
                    "timestamp": now_sec,
                    "contract_type": "PERPETUAL",
                    "funding_countdown": time_to_funding_min
                })
        except Exception as e:
            print(f"[MEXC WARNING] Error processing {symbol}: {e}")
            continue

    print(f"[MEXC] Filtered pairs: {len(results)}")
    return results
