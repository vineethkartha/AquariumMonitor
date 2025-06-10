# gpio_client.py
import socket
import json

SOCKET_PATH = "/tmp/gpio.sock"

def send_command(command, name, pin=None, state=None):
    msg = {
        "command": command,
        "name": name,
        "pin": pin,
        "state": state
    }

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(json.dumps(msg).encode())
        data = client.recv(1024)

    return json.loads(data.decode())

def register(name, pin):
    return send_command("register", name, pin=pin)

def set_gpio(name, state):
    return send_command("set", name, state=state)

def get_gpio(name):
    return send_command("get", name)
