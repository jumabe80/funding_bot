# funding_scanner.py
# --------------------------------------
# Funding Scanner (múltiples exchanges)
# --------------------------------------
# Este módulo ejecuta escaneos secuenciales sobre
# todos los exchanges activos y agrupa las
# oportunidades en una sola vista.
# --------------------------------------

from binance import get_binance_funding_rates
from coinglass_funding_bot import get_coinglass_funding_rates
# from bybit import get_bybit_funding_rates  # (Aún no disponible)

def scan_all_exchanges():
    """
    Escanea todos los exchanges soportados.
    Retorna una lista combinada de oportunidades.
    """
    print("\n==============================")
    print("Iniciando escaneo de exchanges...")
    print("==============================\n")

    all_results = []

    # Binance
    try:
        binance_results = get_binance_funding_rates()
        print(f"[Binance] Pares encontrados: {len(binance_results)}")
        all_results.extend(binance_results)
    except Exception as e:
        print(f"[ERROR] Binance: {e}")

    print("------------------------------")

    # CoinGlass
    try:
        coinglass_results = get_coinglass_funding_rates()
        print(f"[CoinGlass] Pares encontrados: {len(coinglass_results)}")
        all_results.extend(coinglass_results)
    except Exception as e:
        print(f"[ERROR] CoinGlass: {e}")

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
            print(f"[{fr['exchange']}] {fr['symbol']}: {fr['funding_rate']*100:.4f}% | Volumen 24h: {volumen}")
        print("------------------------------")
        print(f"Total oportunidades: {len(results)}")
