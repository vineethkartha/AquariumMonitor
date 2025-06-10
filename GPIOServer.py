# GPIOServer.py
import socket
import os
import json
import lgpio
import threading

SOCKET_PATH = "/tmp/gpio.sock"
CHIP = lgpio.gpiochip_open(0)

registered_pins = {}  # {'white': 6, 'rgb': 5}
pin_states = {}       # {'white': True, ...}

def handle_client(conn):
    with conn:
        data = conn.recv(1024)
        if not data:
            return
        try:
            msg = json.loads(data.decode())
            cmd = msg.get("command")
            name = msg.get("name")
            pin = msg.get("pin")
            state = msg.get("state")

            if cmd == "register":
                if name in registered_pins:
                    response = {"error": "Already registered"}
                else:
                    lgpio.gpio_claim_output(CHIP, pin, 0)
                    registered_pins[name] = pin
                    pin_states[name] = False
                    response = {"status": f"Registered '{name}' on GPIO {pin}"}

            elif cmd == "set":
                if name not in registered_pins:
                    response = {"error": "Not registered"}
                else:
                    lgpio.gpio_write(CHIP, registered_pins[name], int(state))
                    pin_states[name] = bool(state)
                    response = {"status": f"Set '{name}' to {state}"}

            elif cmd == "get":
                if name not in registered_pins:
                    response = {"error": "Not registered"}
                else:
                    val = lgpio.gpio_read(CHIP, registered_pins[name])
                    response = {"state": bool(val)}

            else:
                response = {"error": "Unknown command"}

        except Exception as e:
            response = {"error": str(e)}

        conn.sendall(json.dumps(response).encode())

def run_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(SOCKET_PATH)
        server.listen()
        print(f"GPIO Server listening on {SOCKET_PATH}...")

        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    run_server()
