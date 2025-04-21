# funding_scanner.py
import time
from binance_funding_bot import get_binance_funding_rates
from bybit_funding_bot import get_bybit_funding_rates
from okx_funding_bot import get_okx_funding_rates

def main():
    print("==============================")
    print("Iniciando escaneo de exchanges...")
    print("==============================")

    all_results = []

    # Binance
    binance_data = get_binance_funding_rates()
    print(f"[Binance] Pares filtrados: {len(binance_data)}")
    all_results.extend(binance_data)

    # Bybit
    bybit_data = get_bybit_funding_rates()
    print(f"[Bybit] Pares filtrados: {len(bybit_data)}")
    all_results.extend(bybit_data)

    # OKX
    okx_data = get_okx_funding_rates()
    print(f"[OKX] Pares filtrados: {len(okx_data)}")
    all_results.extend(okx_data)

    print("==============================")
    print("\n✅ Oportunidades encontradas:")
    print("------------------------------")

    if all_results:
        for entry in all_results:
            print(f"[{entry['exchange']}] {entry['symbol']}: {entry['funding_rate']*100:.4f}% | Volumen 24h: ${entry['volume_24h']:,} | Tipo: {entry['contract_type']}")
            print("------------------------------")
    else:
        print("NO PAIR FOUND")

    print(f"Total oportunidades: {len(all_results)}")

if __name__ == "__main__":
    main()
