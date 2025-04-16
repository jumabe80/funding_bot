from binance_funding_bot import get_binance_funding_rates
from bybit_funding_bot import get_bybit_funding_rates
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD

def scan_all_exchanges():
    print("\n==============================")
    print("Iniciando escaneo de exchanges...")
    print("==============================\n")

    all_results = []

    try:
        binance_results = get_binance_funding_rates()
        filtered_binance = [pair for pair in binance_results if pair["funding_rate"] >= FUNDING_RATE_THRESHOLD and pair["volume_24h"] >= VOLUME_24H_THRESHOLD]
        print(f"[Binance] Pares filtrados: {len(filtered_binance)}")
        all_results.extend(filtered_binance)
    except Exception as e:
        print(f"[ERROR] Binance: {e}")

    print("------------------------------")

    try:
        bybit_results = get_bybit_funding_rates()
        filtered_bybit = [pair for pair in bybit_results if pair["funding_rate"] >= FUNDING_RATE_THRESHOLD and pair["volume_24h"] >= VOLUME_24H_THRESHOLD]
        print(f"[Bybit] Pares filtrados: {len(filtered_bybit)}")
        all_results.extend(filtered_bybit)
    except Exception as e:
        print(f"[ERROR] Bybit: {e}")

    print("==============================")
    return all_results

if __name__ == "__main__":
    results = scan_all_exchanges()

    if not results:
        print("\n❌ NO PAIR FOUND across all exchanges")
    else:
        print("\n✅ Oportunidades encontradas:")
        print("------------------------------")
        for fr in sorted(results, key=lambda x: x['funding_rate'], reverse=True):
            volumen = f"${fr['volume_24h']:,.0f}" if fr['volume_24h'] > 0 else "(sin volumen)"
            tipo = f"| Tipo: {fr.get('contract_type', 'N/A')}"
            print(f"[{fr['exchange']}] {fr['symbol']}: {fr['funding_rate']*100:.4f}% | Volumen 24h: {volumen} {tipo}")
        print("------------------------------")
        print(f"Total oportunidades: {len(results)}")
