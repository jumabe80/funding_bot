# notifier.py
import requests

def send_whatsapp_notification(exchange, symbol, funding_rate, volume, countdown):
    phone = "34627829050"
    apikey = "5895653"

    text = (
        f"\ud83d\ude80 Funding Opportunity!\n"
        f"Exchange: {exchange}\n"
        f"Pair: {symbol}\n"
        f"Funding Rate: {funding_rate*100:.4f}%\n"
        f"Volume: ${volume:,}\n"
        f"Funding in: {countdown} min"
    )

    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={requests.utils.quote(text)}&apikey={apikey}"

    try:
        response = requests.get(url, timeout=10)
        if "OK" in response.text:
            print("[NOTIFIER] WhatsApp message sent successfully")
        else:
            print(f"[NOTIFIER WARNING] WhatsApp message may not have been sent: {response.text}")
    except Exception as e:
        print(f"[NOTIFIER ERROR] Failed to send WhatsApp message: {e}")

def notify_if_needed(entry):
    if entry["exchange"] in ["Bitget", "KuCoin", "OKX"] and entry.get("funding_countdown", 9999) <= 30:
        send_whatsapp_notification(
            entry["exchange"],
            entry["symbol"],
            entry["funding_rate"],
            entry["volume_24h"],
            entry["funding_countdown"]
        )
