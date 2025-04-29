# kucoin_funding_bot.py (FIXED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def get_kucoin_funding_rates():
    url = "https://api-futures.kucoin.com/api/v1/contracts/active"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        contracts = response.json().get("data", [])
    except Exception as e:
        print(f"[KUCOIN ERROR] Failed to fetch contracts: {e}")
        return []

    results = []
    now_ms = int(time.time() * 1000)

    for contract in contracts:
        try:
            symbol = contract.get("symbol")
            if not symbol:
                continue

            funding_rate = contract.get("fundingFeeRate")
            volume = contract.get("volumeOf24h")
            mark_price = contract.get("markPrice")
            next_funding_ts = contract.get("nextFundingRateTime")
            open_interest = contract.get("openInterest")

            if None in (funding_rate, volume, next_funding_ts):
                continue

            try:
                funding_rate = float(funding_rate)
                volume = float(volume)
                mark_price = float(mark_price)
                next_funding_ts = int(next_funding_ts)
                open_interest = int(open_interest)
            except:
                continue

            time_to_funding_min = int((next_funding_ts - now_ms) / 60000)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "KuCoin",
                    "symbol": symbol.replace("USDTM", "-USDT-PERP"),
                    "funding_rate": funding_rate,
                    "volume_24h": volume * mark_price,
                    "timestamp": now_ms,
                    "contract_type": "PERPETUAL",
                    "time_to_funding_min": time_to_funding_min
                })
        except Exception as e:
            print(f"[KUCOIN WARNING] Error parsing contract {symbol}: {e}")
            continue

    print(f"[KuCoin] Filtered pairs: {len(results)}")
    return results
