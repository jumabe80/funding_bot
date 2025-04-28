# quick_test_table.py (only KuCoin contract sampling)
import requests
import random
import time

KEY_FIELDS = [
    "symbol", "fundingFeeRate", "predictedFundingFeeRate", "turnoverOf24h",
    "volumeOf24h", "markPrice", "openInterest", "nextFundingRateTime"
]

def quick_test_table():
    try:
        market_response = requests.get("https://api-futures.kucoin.com/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        print(f"[KUCOIN] {len(contracts)} contracts fetched.")

        if not contracts:
            print("[KUCOIN] No contracts available.")
            return

        sample_contracts = random.sample(contracts, min(5, len(contracts)))

        print("\n========= SAMPLE CONTRACTS =========")
        for contract in sample_contracts:
            print("\n----------------------------------------")
            for field in KEY_FIELDS:
                value = contract.get(field, "N/A")
                print(f"{field}: {value}")
            print("----------------------------------------")
            time.sleep(0.1)

        print("========= END SAMPLE =========\n")

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    quick_test_table()
