import websocket
import json
import ssl
from threading import Thread

latest_prices = {}

def on_message(ws, message):
    data = json.loads(message)
    symbol = data['s']
    price = data['c']
    latest_prices[symbol] = price
    print(f"{symbol}: {price}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")

def connect_to_websocket(symbols):
    socket = f"wss://stream.binance.com:9443/ws/{'/'.join(symbols)}@ticker"
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def start_websocket(symbols):
    websocket_thread = Thread(target=connect_to_websocket, args=(symbols,))
    websocket_thread.daemon = True
    websocket_thread.start()

if __name__ == "__main__":
    symbols = ["btcusdt", "ethusdt", "dogeusdt"]
    start_websocket(symbols)
    
    # Keep the main thread running
    import time
    while True:
        time.sleep(1)