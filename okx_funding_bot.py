# okx_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_okx_funding_rates():
    base_url = "https://www.okx.com"
    tickers_url = f"{base_url}/api/v5/market/tickers?instType=SWAP"
    funding_url = f"{base_url}/api/v5/public/funding-rate"

    try:
        tickers_response = requests.get(tickers_url, timeout=10)
        tickers_data = tickers_response.json().get("data", [])
        now = int(time.time() * 1000)
        results = []

        for ticker in tickers_data:
            inst_id = ticker.get("instId")  # example: BTC-USDT-SWAP
            quote_volume = float(ticker.get("quoteVol24h", 0))

            if quote_volume < VOLUME_24H_THRESHOLD:
                continue

            funding_resp = requests.get(f"{funding_url}?instId={inst_id}", timeout=10)
            if funding_resp.status_code != 200:
                continue

            funding_data = funding_resp.json().get("data", [{}])[0]
            if not funding_data:
                continue

            funding_rate = float(funding_data.get("fundingRate", 0))

            if funding_rate >= FUNDING_RATE_THRESHOLD:
                results.append({
                    "exchange": "OKX",
                    "symbol": inst_id,
                    "funding_rate": funding_rate,
                    "volume_24h": quote_volume,
                    "timestamp": now,
                    "contract_type": "PERPETUAL"
                })

            time.sleep(0.25)  # To respect rate limits

        return results

    except Exception as e:
        print(f"[ERROR OKX] {e}")
        return []
