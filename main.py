import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
import time
import os
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": texto
    }

    response = requests.get(url, params=params)
    print("Respuesta Telegram:", response.text)

def analizar_accion(ticker):
    data = yf.download(ticker, period="1d", interval="5m")

    if data.empty:
        return

    close_prices = data['Close'].squeeze()

    rsi = RSIIndicator(close=close_prices, window=14).rsi()
    ultimo_rsi = rsi.iloc[-1]
    precio = close_prices.iloc[-1]

    if ultimo_rsi < 30:
        señal = "🟢 COMPRAR"
    elif ultimo_rsi > 70:
        señal = "🔴 VENDER"
    else:
        señal = "🟡 ESPERAR"

    mensaje = f"{ticker} | Precio: {precio:.2f} | RSI: {ultimo_rsi:.2f} | {señal}"
    enviar_mensaje(mensaje)

acciones = ["AAPL", "TSLA", "MSFT"]
enviar_mensaje("🚀 AxisPulse ya está funcionando")
while True:
    for accion in acciones:
        analizar_accion(accion)

    time.sleep(300)
