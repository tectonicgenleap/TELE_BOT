import websocket
import json
import ssl
from threading import Thread
import time

latest_prices = {}
symbols = []

def on_message(ws, message):
    try:
        data = json.loads(message)
        if 's' in data and 'c' in data:
            symbol = data['s']
            price = data['c']
            latest_prices[symbol] = price
            print(f"{symbol}: {price}")
        else:
            print(f"Unexpected message format: {message}")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {message}")
    except Exception as e:
        print(f"Error in on_message: {e}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("WebSocket connection opened")
    
    # Subscribe to individual ticker streams
    for symbol in symbols:
        subscribe_msg = json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol.lower()}@ticker"], "id": 1})
        ws.send(subscribe_msg)

def connect_to_websocket():
    socket = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def start_websocket():
    while True:
        try:
            connect_to_websocket()
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
        print("Attempting to reconnect in 5 seconds...")
        time.sleep(5)

def init_websocket(symbol_list):
    global symbols
    symbols = symbol_list
    websocket_thread = Thread(target=start_websocket)
    websocket_thread.daemon = True
    websocket_thread.start()

if __name__ == "__main__":
    test_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "DOGEUSDT", "SOLUSDT"]
    init_websocket(test_symbols)
    
    # Keep the main thread running
    while True:
        time.sleep(1)