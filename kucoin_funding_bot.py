# kucoin_funding_bot.py (FIXED VOLUME FILTER + CORRECT FUNDING COUNTDOWN)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD
# from notifier import send_whatsapp_message

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
            volume_base = contract.get("volumeOf24h")
            mark_price = contract.get("markPrice")
            next_funding_ts = contract.get("nextFundingRateTime")
            open_interest = contract.get("openInterest")

            if None in (funding_rate, volume_base, mark_price, next_funding_ts):
                continue

            try:
                funding_rate = float(funding_rate)
                volume_base = float(volume_base)
                mark_price = float(mark_price)
                next_funding_ts = int(next_funding_ts)
                open_interest = int(open_interest)
            except:
                continue

            volume_usdt = volume_base * mark_price

            # Calculate funding countdown in minutes (fixed correctly)
            now_sec = int(time.time())
           # time_to_funding_min = int((next_funding_ts - now_sec) / 60)
             time_to_funding_min = int((next_funding_ts)/60)

            if funding_rate >= FUNDING_RATE_THRESHOLD and volume_usdt >= VOLUME_24H_THRESHOLD:
                results.append({
                    "exchange": "KuCoin",
                    "symbol": symbol.replace("USDTM", "-USDT-PERP"),
                    "funding_rate": funding_rate,
                    "volume_24h": round(volume_usdt),
                    "timestamp": now_ms,
                    "contract_type": "PERPETUAL",
                    "funding_countdown": time_to_funding_min
                })
        except Exception as e:
            print(f"[KUCOIN WARNING] Error parsing contract {symbol}: {e}")
            continue

    print(f"[KuCoin] Filtered pairs: {len(results)}")
    return results
