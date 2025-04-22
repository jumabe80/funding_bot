# quick_test.py (DEBUG VERSION)
import requests
import time

FUNDING_RATE_THRESHOLD = 0.0003  # Example 0.03%
VOLUME_24H_THRESHOLD = 10000000    # Example $10M

def quick_test_bybit_okx():
    results = {"Bybit": 0, "OKX": 0}

    # BYBIT
    try:
        tickers_response = requests.get("https://api.bybit.com/v5/market/tickers?category=linear", timeout=10)
        tickers_data = tickers_response.json().get("result", {}).get("list", [])
        now = int(time.time() * 1000)

        print("\n[BYBIT DEBUG] Showing funding and volume for each pair:")
        for ticker in tickers_data:
            symbol = ticker.get("symbol")
            turnover = float(ticker.get("turnover24h", 0))
            funding_rate = float(ticker.get("fundingRate", 0))

            # DEBUG print
            print(f"[BYBIT] {symbol} | Funding Rate: {funding_rate:.6f} | Volume 24h: ${turnover:,.2f}")

            if turnover >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
                results["Bybit"] += 1

    except Exception as e:
        results["Bybit"] = f"Error: {e}"

    # OKX
    try:
        tickers_response = requests.get("https://www.okx.com/api/v5/market/tickers?instType=SWAP", timeout=10)
        tickers_data = tickers_response.json().get("data", [])
        now = int(time.time() * 1000)

        print("\n[OKX DEBUG] Showing funding and volume for each pair:")
        for ticker in tickers_data:
            inst_id = ticker.get("instId")
            quote_volume_raw = ticker.get("quoteVol24h")

            if quote_volume_raw is None:
                continue

            quote_volume = float(quote_volume_raw)

            # Fetch funding rate for this instrument
            funding_response = requests.get(f"https://www.okx.com/api/v5/public/funding-rate?instId={inst_id}", timeout=10)
            if funding_response.status_code != 200:
                continue

            funding_json = funding_response.json()
            if funding_json.get("code") != "0" or not funding_json.get("data"):
                continue

            funding_data = funding_json.get("data", [{}])[0]
            funding_rate = float(funding_data.get("fundingRate", 0))

            # DEBUG print
            print(f"[OKX] {inst_id} | Funding Rate: {funding_rate:.6f} | Volume 24h: ${quote_volume:,.2f}")

            if quote_volume >= VOLUME_24H_THRESHOLD and funding_rate >= FUNDING_RATE_THRESHOLD:
                results["OKX"] += 1

            time.sleep(0.25)
    except Exception as e:
        results["OKX"] = f"Error: {e}"

    return results

if __name__ == "__main__":
    print("\n========= QUICK TEST START =========")
    print(quick_test_bybit_okx())
    print("========= QUICK TEST END =========\n")
