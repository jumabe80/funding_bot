# okx_funding_bot.py (UPDATED WITH FUNDING COUNTDOWN)
import requests
import time
from datetime import datetime
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_okx_funding_rates():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"
    try:
        tickers_response = requests.get(url, timeout=10)
        tickers_data = tickers_response.json().get("data", [])
    except Exception as e:
        print(f"[ERROR OKX] Failed to fetch tickers: {e}")
        return []

    results = []

    for ticker in tickers_data:
        inst_id = ticker.get("instId")
        quote_volume_raw = ticker.get("volCcy24h")

        try:
            quote_volume = float(quote_volume_raw) if quote_volume_raw else 0
        except ValueError:
            quote_volume = 0

        funding_url = f"https://www.okx.com/api/v5/public/funding-rate?instId={inst_id}"
        try:
            funding_response = requests.get(funding_url, timeout=10)
            if funding_response.status_code != 200:
                continue
            funding_json = funding_response.json()
            if funding_json.get("code") != "0" or not funding_json.get("data"):
                continue
            funding_data = funding_json["data"][0]
            funding_rate = float(funding_data.get("fundingRate", 0))

            # Compute funding countdown in minutes
            next_ts = int(funding_data.get("nextFundingTime", 0))
            now_ts = int(time.time() * 1000)
            minutes_until = max((next_ts - now_ts) // 60000, 0)

        except Exception:
            continue

        if quote_volume >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
            results.append({
                "exchange": "OKX",
                "symbol": inst_id,
                "funding_rate": funding_rate,
                "volume_24h": quote_volume,
                "contract_type": "PERPETUAL",
                "funding_countdown": minutes_until
            })

        time.sleep(0.25)

    print(f"[OKX] Pares filtrados: {len(results)}")
    return results
