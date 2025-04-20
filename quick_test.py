import requests
import time

FUNDING_RATE_THRESHOLD = 0.0005  # Example 0.05%
VOLUME_24H_THRESHOLD = 20000000   # Example $20M

def quick_test_bybit_okx():
    results = {"Bybit": 0, "OKX": 0}
    
    # BYBIT
    try:
        tickers = requests.get("https://api.bybit.com/v5/market/tickers?category=linear", timeout=10).json()
        symbols = [item["symbol"] for item in tickers.get("result", {}).get("list", [])]
        for symbol in symbols[:10]:  # limit to 10 to avoid rate limits
            funding = requests.get(f"https://api.bybit.com/v5/market/funding/prev-funding-rate?symbol={symbol}", timeout=10).json()
            funding_rate = float(funding.get("result", {}).get("fundingRate", 0))
            turnover = float(next((item["turnover24h"] for item in tickers.get("result", {}).get("list", []) if item["symbol"] == symbol), 0))
            if funding_rate >= FUNDING_RATE_THRESHOLD and turnover >= VOLUME_24H_THRESHOLD:
                results["Bybit"] += 1
            time.sleep(0.2)
    except Exception as e:
        results["Bybit"] = f"Error: {e}"
    
    # OKX
    try:
        tickers = requests.get("https://www.okx.com/api/v5/market/tickers?instType=SWAP", timeout=10).json()
        symbols = [item["instId"] for item in tickers.get("data", [])]
        for symbol in symbols[:10]:  # limit to 10
            funding = requests.get(f"https://www.okx.com/api/v5/public/funding-rate?instId={symbol}", timeout=10).json()
            funding_rate = float(funding.get("data", [{}])[0].get("fundingRate", 0))
            turnover = float(next((item["quoteVol24h"] for item in tickers.get("data", []) if item["instId"] == symbol), 0))
            if funding_rate >= FUNDING_RATE_THRESHOLD and turnover >= VOLUME_24H_THRESHOLD:
                results["OKX"] += 1
            time.sleep(0.2)
    except Exception as e:
        results["OKX"] = f"Error: {e}"
    
    return results

if __name__ == "__main__":
    print(quick_test_bybit_okx())
