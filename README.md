# Funding Bot

Escáner de oportunidades de arbitraje de funding rates en exchanges de futuros perpetuos.

## 📁 Estructura del proyecto

```
funding-bot/
├── funding_scanner.py          # Archivo principal que ejecuta el escaneo
├── binance_funding_bot.py      # Scraper de Binance funding
├── bybit_funding_bot.py        # Placeholder (para futura integración Bybit)
├── settings.py                 # Umbrales configurables
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

---

## 🚀 Cómo usar

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/funding-bot.git
cd funding-bot
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el bot
```bash
python3 funding_scanner.py
```

---

## ⚙️ Configuración
Edita `settings.py` para modificar los umbrales de filtro:

```python
FUNDING_RATE_THRESHOLD = 0.0003       # Mínimo funding rate (ej: 0.03%)
VOLUME_24H_THRESHOLD = 10000000       # Mínimo volumen 24h (ej: $10M)
```

---

## 📈 Próximos pasos
- Agregar integración real con Bybit
- Incorporar CoinGlass para múltiples exchanges
- Implementar alertas automáticas
- Ejecutar periódicamente con cron o script

---

Desarrollado por Juan · 2025
