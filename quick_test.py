# quick_test.py (KUCOIN ONLY ACTIVE, OTHERS COMMENTED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD


def quick_test():
    results = {"Bybit": 0, "OKX": 0, "KuCoin": 0}

    # KUCOIN (ACTIVE)
    try:
        market_response = requests.get("https://api-futures.kucoin.com/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        print("[KUCOIN] Contracts fetched.")

        for contract in contracts:
            symbol = contract.get("symbol")
            if not symbol:
                continue

            funding_resp = requests.get(f"https://api-futures.kucoin.com/api/v1/funding-rate/{symbol}", timeout=10)
            funding_data = funding_resp.json().get("data", {})

            funding_rate_str = funding_data.get("value")
            if funding_rate_str in [None, ""]:
                continue

            try:
                funding_rate = float(funding_rate_str)
            except ValueError:
                continue

            print(f"[KUCOIN] {symbol} | Funding Rate: {funding_rate:.6f}")

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
