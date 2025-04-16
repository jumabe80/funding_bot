# funding_scanner.py
# --------------------------------------
# Funding Scanner (múltiples exchanges)
# --------------------------------------
# Este módulo ejecuta escaneos secuenciales sobre
# todos los exchanges activos y agrupa las
# oportunidades en una sola vista.
# --------------------------------------

from binance_funding_bot import get_binance_funding_rates
from coinglass_funding_bot import get_coinglass_funding_rates
from settings import FUNDING_RATE_THRESHOLD, VOLUME_24H_THRESHOLD
# from bybit import get_bybit_funding_rates  # (Aún no disponible)

def scan_all_exchanges():
    """
    Escanea todos los exchanges soportados.
    Retorna una lista combinada de oportunidades filtradas.
    """
    print("\n==============================")
    print("Iniciando escaneo de exchanges...")
    print("==============================\n")

    all_results = []

    # Binance
    try:
        binance_results = get_binance_funding_rates()
        filtered_binance = [pair for pair in binance_results if pair["funding_rate"] >= FUNDING_RATE_THRESHOLD and pair["volume_24h"] >= VOLUME_24H_THRESHOLD]
        print(f"[Binance] Pares filtrados: {len(filtered_binance)}")
        all_results.extend(filtered_binance)
    except Exception as e:
        print(f"[ERROR] Binance: {e}")

    print("------------------------------")

    # CoinGlass (sin volumen, solo filtro por funding)
    try:
        coinglass_results = get_coinglass_funding_rates()
        print(f"[DEBUG] CoinGlass raw total tokens: {len(coinglass_results)}")
        filtered_coinglass = [pair for pair in coinglass_results if pair["funding_rate"] >= FUNDING_RATE_THRESHOLD]
        print(f"[CoinGlass] Pares filtrados: {len(filtered_coinglass)}")
        all_results.extend(filtered_coinglass)
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
            tipo = f"| Tipo: {fr.get('contract_type', 'N/A')}"
            print(f"[{fr['exchange']}] {fr['symbol']}: {fr['funding_rate']*100:.4f}% | Volumen 24h: {volumen} {tipo}")
        print("------------------------------")
        print(f"Total oportunidades: {len(results)}")
