# quick_test_table.py (KUCOIN SAMPLE 50 CONTRACTS)
import requests
import random
import time

def quick_test_kucoin_sample():
    try:
        market_response = requests.get("https://api-futures.kucoin.com/api/v1/contracts/active", timeout=10)
        contracts = market_response.json().get("data", [])

        if not contracts:
            print("No contracts found.")
            return

        print(f"[KUCOIN] Total contracts fetched: {len(contracts)}")

        # Pick 50 random contracts
        random_contracts = random.sample(contracts, min(50, len(contracts)))

        print("\nSample of 50 KuCoin USDT-M Perpetual Contracts:")
        print("="*80)

        for contract in random_contracts:
            symbol = contract.get("symbol", "N/A")
            funding_fee_rate = contract.get("fundingFeeRate", "N/A")
            turnover_24h = contract.get("turnoverOf24h", "N/A")
            volume_24h = contract.get("volumeOf24h", "N/A")
            mark_price = contract.get("markPrice", "N/A")
            open_interest = contract.get("openInterest", "N/A")
            next_funding_time = contract.get("nextFundingRateTime", "N/A")

            print(f"Symbol: {symbol}")
            print(f"Funding Fee Rate: {funding_fee_rate}")
            print(f"24h Turnover: {turnover_24h}")
            print(f"24h Volume: {volume_24h}")
            print(f"Mark Price: {mark_price}")
            print(f"Open Interest: {open_interest}")
            print(f"Next Funding Rate Time: {next_funding_time}")
            print("-"*80)

            time.sleep(0.05)  # Light delay to prevent spamming

    except Exception as e:
        print(f"Error during KuCoin quick test: {e}")

if __name__ == "__main__":
    quick_test_kucoin_sample()
