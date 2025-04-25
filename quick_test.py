# quick_test.py (KUCOIN ONLY ACTIVE, OTHERS COMMENTED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def quick_test():
    results = {"Bybit": 0, "OKX": 0, "KuCoin": 0}

    # KUCOIN (ACTIVE)
    try:
        market_response = requests.get("https://api-futures.kucoin.com/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        print("[KUCOIN DEBUG] Contracts fetched:")
        print(contracts)

        for contract in contracts:
            symbol = contract.get("symbol")
            if not symbol:
                continue

            # Normalize symbol for KuCoin ticker API
            if symbol.endswith('USDTM'):
                contract_id = symbol.replace('USDTM', '-USDTM')
            else:
                contract_id = symbol

            ticker_url = f"https://api-futures.kucoin.com/api/v1/contract/market/ticker?symbol={contract_id}"
            ticker_resp = requests.get(ticker_url, timeout=10)
            ticker_data = ticker_resp.json().get("data", {})

            if not ticker_data:
                print(f"[KUCOIN WARNING] Empty ticker for {contract_id}, skipping.")
                continue

            print(f"[KUCOIN DEBUG] Ticker for {contract_id}: {ticker_data}")

            quote_volume = float(ticker_data.get("turnoverOf24h", 0))
            if quote_volume < VOLUME_24H_THRESHOLD:
                continue

            funding_resp = requests.get(f"https://api-futures.kucoin.com/api/v1/funding-rate/{contract_id}", timeout=10)
            funding_data = funding_resp.json().get("data", {})
            print(f"[KUCOIN DEBUG] Funding rate for {contract_id}: {funding_data}")

            funding_rate_str = funding_data.get("value")
            if funding_rate_str in [None, ""]:
                continue

            try:
                funding_rate = float(funding_rate_str)
            except ValueError:
                continue

            if funding_rate >= FUNDING_RATE_THRESHOLD:
                results["KuCoin"] += 1

            time.sleep(0.1)

    except Exception as e:
        results["KuCoin"] = f"Error: {e}"

    print("========= QUICK TEST START =========")
    print(results)
    print("========= QUICK TEST END =========")

if __name__ == "__main__":
    quick_test()
