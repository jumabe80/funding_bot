# quick_test_table.py (MEXC SAMPLE 100 CONTRACTS)
import requests
import random
import time

def quick_test_mexc_sample():
    try:
        response = requests.get("https://contract.mexc.com/api/v1/contract/detail", timeout=10)
        contracts = response.json().get("data", [])

        if not contracts:
            print("No contracts found.")
            return

        print(f"[MEXC] Total contracts fetched: {len(contracts)}")

        # Pick 100 random contracts
        random_contracts = random.sample(contracts, min(100, len(contracts)))

        print("\nSample of 100 MEXC USDT-M Perpetual Contracts:")
        print("="*80)

        for contract in random_contracts:
            symbol = contract.get("symbol", "N/A")
            funding_rate = contract.get("fundingRate", "N/A")
            turnover_24h = contract.get("turnover", "N/A")
            volume_24h = contract.get("volume", "N/A")
            mark_price = contract.get("lastPrice", "N/A")
            open_interest = contract.get("holdVol", "N/A")
            next_funding_time = contract.get("fundingTime", "N/A")

            print(f"Symbol: {symbol}")
            print(f"Funding Rate: {funding_rate}")
            print(f"24h Turnover: {turnover_24h}")
            print(f"24h Volume: {volume_24h}")
            print(f"Mark Price: {mark_price}")
            print(f"Open Interest: {open_interest}")
            print(f"Next Funding Time: {next_funding_time}")
            print("-"*80)

            time.sleep(0.05)

    except Exception as e:
        print(f"Error during MEXC quick test: {e}")

if __name__ == "__main__":
    quick_test_mexc_sample()
