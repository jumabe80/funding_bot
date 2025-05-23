# funding_scanner.py (UPDATED TO ADD MEXC)
from binance_funding_bot import get_binance_funding_rates
from bybit_funding_bot import get_bybit_funding_rates
from okx_funding_bot import get_okx_funding_rates
from bitget_funding_bot import get_bitget_funding_rates
from kucoin_funding_bot import get_kucoin_funding_rates
from deribit_funding_bot import get_deribit_funding_rates
from mexc_funding_bot import get_mexc_funding_rates
from collections import defaultdict

def main():
    print("=" * 30)
    print("Starting exchange scan...")
    print("=" * 30)

    all_results = []

    binance_data = get_binance_funding_rates()
    bybit_data = get_bybit_funding_rates()
    okx_data = get_okx_funding_rates()
    bitget_data = get_bitget_funding_rates()
    kucoin_data = get_kucoin_funding_rates()
    deribit_data = get_deribit_funding_rates()
    mexc_data = get_mexc_funding_rates()

    print(f"[Binance] Filtered pairs: {len(binance_data)}")
    print(f"[Bybit] Filtered pairs: {len(bybit_data)}")
    print(f"[OKX] Filtered pairs: {len(okx_data)}")
    print(f"[Bitget] Filtered pairs: {len(bitget_data)}")
    print(f"[KuCoin] Filtered pairs: {len(kucoin_data)}")
    print(f"[Deribit] Filtered pairs: {len(deribit_data)}")
    print(f"[MEXC] Filtered pairs: {len(mexc_data)}")

    all_results.extend(binance_data)
    all_results.extend(bybit_data)
    all_results.extend(okx_data)
    all_results.extend(bitget_data)
    all_results.extend(kucoin_data)
    all_results.extend(deribit_data)
    all_results.extend(mexc_data)

    if not all_results:
        print("NO PAIR FOUND")
        return

    # Group results by exchange
    grouped = defaultdict(list)
    for entry in all_results:
        grouped[entry['exchange']].append(entry)

    print("\n✅ Opportunities found:")
    print("-" * 30)

    for exchange in sorted(grouped.keys()):
        sorted_entries = sorted(
            grouped[exchange],
            key=lambda x: (x.get("funding_countdown", float('inf')), -x.get("funding_rate", 0))
        )
        for entry in sorted_entries:
            countdown_display = f" | Funding in {entry['funding_countdown']} min" if 'funding_countdown' in entry and entry['funding_countdown'] is not None else ""
            print(
                f"[{entry['exchange']}] {entry['symbol']}: {entry['funding_rate']*100:.4f}% "
                f"| 24h Volume: ${entry['volume_24h']:,} | Type: {entry['contract_type']}{countdown_display}"
            )
            print("-" * 30)

if __name__ == "__main__":
    main()
