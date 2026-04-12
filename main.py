import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
import time
import os
from telegram import Bot

TOKEN = os.getenv("8252991488:AAFPTelZU_uQOgMvjkA2RWfMyB0siWcWwkc")
CHAT_ID = os.getenv("8626753364")

bot = Bot(token="8252991488:AAFPTelZU_uQOgMvjkA2RWfMyB0siWcWwkc")

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
    bot.send_message(chat_id=CHAT_ID, text=mensaje)

acciones = ["AAPL", "TSLA", "MSFT"]

while True:
    for accion in acciones:
        analizar_accion(accion)
    
    time.sleep(300)
