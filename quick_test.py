# quick_test.py (FINAL POLISHED VERSION)
import requests
import time
from datetime import datetime

FUNDING_RATE_THRESHOLD = 0.00005  # 0.005%
VOLUME_24H_THRESHOLD = 1000000    # $1M

def quick_test_bybit_okx():
    results = {"Bybit": 0, "OKX": 0}

    # BYBIT
    try:
        tickers_response = requests.get("https://api.bybit.com/v5/market/tickers?category=linear", timeout=10)
        tickers_data = tickers_response.json().get("result", {}).get("list", [])

        print("\n[BYBIT DEBUG] Showing funding and volume for each pair:")
        for ticker in tickers_data:
            symbol = ticker.get("symbol")
            turnover = float(ticker.get("turnover24h", 0))
            funding_rate_raw = ticker.get("fundingRate")

            if not funding_rate_raw:
                continue

            try:
                funding_rate = float(funding_rate_raw)
            except ValueError:
                continue

            print(f"[BYBIT] {symbol} | Funding Rate: {funding_rate:.6f} | Volume 24h: ${turnover:,.2f}")

            if turnover >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
                results["Bybit"] += 1

    except Exception as e:
        results["Bybit"] = f"Error: {e}"

    # OKX
    try:
        tickers_response = requests.get("https://www.okx.com/api/v5/market/tickers?instType=SWAP", timeout=10)
        tickers_data = tickers_response.json().get("data", [])

        print("\n[OKX DEBUG] Showing funding and volume for each pair:")
        for ticker in tickers_data:
            inst_id = ticker.get("instId")
            quote_volume_raw = ticker.get("quoteVol24h")

            print(f"[OKX RAW] {inst_id} | Raw Volume: {quote_volume_raw}")

            if quote_volume_raw is None:
                continue

            try:
                quote_volume = float(quote_volume_raw)
            except ValueError:
                continue

            funding_response = requests.get(f"https://www.okx.com/api/v5/public/funding-rate?instId={inst_id}", timeout=10)
            if funding_response.status_code != 200:
                continue

            funding_json = funding_response.json()
            if funding_json.get("code") != "0" or not funding_json.get("data"):
                continue

            funding_data = funding_json.get("data", [{}])[0]
            try:
                funding_rate = float(funding_data.get("fundingRate", 0))
            except ValueError:
                continue

            print(f"[OKX] {inst_id} | Funding Rate: {funding_rate:.6f} | Volume 24h: ${quote_volume:,.2f}")

            if quote_volume >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
                results["OKX"] += 1

            time.sleep(0.25)

    except Exception as e:
        results["OKX"] = f"Error: {e}"

    return results

if __name__ == "__main__":
    print("\n========= QUICK TEST START =========")
    print(f"Scan Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    results = quick_test_bybit_okx()
    print("\n========= QUICK TEST RESULTS =========")
    for k, v in results.items():
        print(f"{k}: {v}")
    print("========= QUICK TEST END =========\n")
