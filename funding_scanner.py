# funding_scanner.py (UPDATED TO ORDER RESULTS BY FUNDING COUNTDOWN, THEN RATE)
from binance_funding_bot import get_binance_funding_rates
from bybit_funding_bot import get_bybit_funding_rates
from okx_funding_bot import get_okx_funding_rates
from collections import defaultdict


def main():
    print("=" * 30)
    print("Iniciando escaneo de exchanges...")
    print("=" * 30)

    all_results = []

    binance_data = get_binance_funding_rates()
    bybit_data = get_bybit_funding_rates()
    okx_data = get_okx_funding_rates()

    all_results.extend(binance_data)
    all_results.extend(bybit_data)
    all_results.extend(okx_data)

    if not all_results:
        print("NO PAIR FOUND")
        return

    # Group results by exchange
    grouped = defaultdict(list)
    for entry in all_results:
        grouped[entry['exchange']].append(entry)

    print("\n✅ Oportunidades encontradas:")
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
                f"| Volumen 24h: ${entry['volume_24h']:,} | Tipo: {entry['contract_type']}{countdown_display}"
            )
            print("-" * 30)

if __name__ == "__main__":
    main()
