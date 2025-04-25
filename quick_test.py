# quick_test.py (KUCOIN ONLY ACTIVE, OTHERS COMMENTED)
import requests
import time
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def quick_test():
    results = {"Bybit": 0, "OKX": 0, "KuCoin": 0}

    # # BYBIT (COMMENTED)
    # try:
    #     tickers_response = requests.get("https://api.bybit.com/v5/market/tickers?category=linear", timeout=10)
    #     tickers_data = tickers_response.json().get("result", {}).get("list", [])
    #     now = int(time.time() * 1000)

    #     for ticker in tickers_data:
    #         symbol = ticker.get("symbol")
    #         turnover = float(ticker.get("turnover24h", 0))
    #         if turnover < VOLUME_24H_THRESHOLD:
    #             continue
    #         funding_response = requests.get(f"https://api.bybit.com/v5/market/funding/prev-funding-rate?symbol={symbol}", timeout=10)
    #         if funding_response.status_code != 200:
    #             continue
    #         funding_json = funding_response.json()
    #         if funding_json.get("retCode") != 0 or not funding_json.get("result"):
    #             continue
    #         funding_rate = float(funding_json.get("result", {}).get("fundingRate", 0))
    #         if funding_rate >= FUNDING_RATE_THRESHOLD:
    #             results["Bybit"] += 1
    #         time.sleep(0.25)
    # except Exception as e:
    #     results["Bybit"] = f"Error: {e}"

    # # OKX (COMMENTED)
    # try:
    #     tickers_response = requests.get("https://www.okx.com/api/v5/market/tickers?instType=SWAP", timeout=10)
    #     tickers_data = tickers_response.json().get("data", [])
    #     now = int(time.time() * 1000)

    #     for ticker in tickers_data:
    #         inst_id = ticker.get("instId")
    #         quote_volume_raw = ticker.get("quoteVol24h")
    #         if quote_volume_raw is None:
    #             continue
    #         quote_volume = float(quote_volume_raw)
    #         if quote_volume < VOLUME_24H_THRESHOLD:
    #             continue
    #         funding_response = requests.get(f"https://www.okx.com/api/v5/public/funding-rate?instId={inst_id}", timeout=10)
    #         if funding_response.status_code != 200:
    #             continue
    #         funding_json = funding_response.json()
    #         if funding_json.get("code") != "0" or not funding_json.get("data"):
    #             continue
    #         funding_data = funding_json.get("data", [{}])[0]
    #         funding_rate = float(funding_data.get("fundingRate", 0))
    #         if funding_rate >= FUNDING_RATE_THRESHOLD:
    #             results["OKX"] += 1
    #         time.sleep(0.25)
    # except Exception as e:
    #     results["OKX"] = f"Error: {e}"

    # KUCOIN (ACTIVE)
    try:
        market_response = requests.get("https://api.kucoin.com/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        for contract in contracts:
            symbol = contract.get("symbol")
            if not symbol:
                continue

            ticker_resp = requests.get(f"https://api.kucoin.com/api/v1/contract/market/ticker?symbol={symbol}", timeout=10)
            ticker_data = ticker_resp.json().get("data", {})
            quote_volume = float(ticker_data.get("turnoverOf24h", 0))
            if quote_volume < VOLUME_24H_THRESHOLD:
                continue

            funding_resp = requests.get(f"https://api.kucoin.com/api/v1/funding-rate/{symbol}", timeout=10)
            funding_data = funding_resp.json().get("data", {})

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
