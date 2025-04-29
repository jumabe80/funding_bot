# deribit_funding_bot.py
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_deribit_funding_rates():
    base_url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
    results = []
    now_ms = int(time.time() * 1000)

    try:
        for currency in ["BTC", "ETH"]:
            response = requests.get(f"{base_url}?currency={currency}&kind=future", timeout=10)
            response.raise_for_status()
            contracts = response.json().get("result", [])

            for contract in contracts:
                try:
                    instrument_name = contract.get("instrument_name")
                    if not instrument_name or not instrument_name.endswith("-PERPETUAL"):
                        continue

                    funding_rate = contract.get("funding_rate", 0)
                    volume = contract.get("volume", 0)
                    mark_price = contract.get("mark_price", 0)
                    open_interest = contract.get("open_interest", 0)

                    # Funding countdown not directly available in Deribit
                    funding_countdown = None

                    if None in (funding_rate, volume, mark_price):
                        continue

                    try:
                        funding_rate = float(funding_rate)
                        volume = float(volume)
                        mark_price = float(mark_price)
                        open_interest = float(open_interest)
                    except:
                        continue

                    if funding_rate >= FUNDING_RATE_THRESHOLD and (volume * mark_price) >= VOLUME_24H_THRESHOLD:
                        results.append({
                            "exchange": "Deribit",
                            "symbol": instrument_name,
                            "funding_rate": funding_rate,
                            "volume_24h": int(volume * mark_price),
                            "timestamp": now_ms,
                            "contract_type": "PERPETUAL",
                            "funding_countdown": funding_countdown
                        })

                except Exception as e:
                    print(f"[DERIBIT WARNING] Error parsing contract {instrument_name}: {e}")
                    continue

    except Exception as e:
        print(f"[DERIBIT ERROR] Failed to fetch contracts: {e}")
        return []

    print(f"[Deribit] Filtered pairs: {len(results)}")
    return results
