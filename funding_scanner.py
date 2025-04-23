# funding_scanner.py (UPDATED TO SHOW FUNDING COUNTDOWN)
from binance_funding_bot import get_binance_funding_rates
from bybit_funding_bot import get_bybit_funding_rates
from okx_funding_bot import get_okx_funding_rates


def main():
    print("=" * 30)
    print("Starting exchange scan...")
    print("=" * 30)

    all_results = []

    binance_data = get_binance_funding_rates()
    all_results.extend(binance_data)

    bybit_data = get_bybit_funding_rates()
    all_results.extend(bybit_data)

    okx_data = get_okx_funding_rates()
    all_results.extend(okx_data)

    if not all_results:
        print("NO PAIR FOUND")
        return

    print("\n✅ Opportunities found:")
    print("-" * 30)

    for entry in all_results:
        countdown_display = f" | Funding in {entry['funding_countdown']} min" if 'funding_countdown' in entry and entry['funding_countdown'] is not None else ""
        print(
            f"[{entry['exchange']}] {entry['symbol']}: {entry['funding_rate']*100:.4f}% "
            f"| Volumen 24h: ${entry['volume_24h']:,} | Tipo: {entry['contract_type']}{countdown_display}"
        )
        print("-" * 30)

if __name__ == "__main__":
    main()
