import socket
import json

SECRET_KEY = "my_secret_key"

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_json(sock, data):
    json_data = json.dumps(data)
    sock.sendall(json_data.encode('utf-8'))

def receive_json(sock):
    try:
        data = sock.recv(1024)
        if not data:
            return None
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
        return None

def authenticate(sock):
    auth_message = {"auth": SECRET_KEY}
    send_json(sock, auth_message)
    response = receive_json(sock)
    if response and response.get("status") == "ok":
        return True
    return False
