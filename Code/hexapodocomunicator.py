import socket
import threading
import time
import json
import datetime

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433
CHECK_INTERVAL = 1  # Aumentado a 1 segundo
TIMEOUT = 1  # Segundos para esperar una respuesta antes de reintentar la conexión
SECRET_KEY = "my_secret_key"  # Clave secreta compartida para autenticación básica

class HexapodCommunicator:
    def __init__(self, name, server_host, send_port, receive_port):
        self.name = name
        self.server_host = server_host
        self.send_port = send_port
        self.receive_port = receive_port
        self.connected = False
        self.socket = None
        self.lock = threading.Lock()

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_json(self, data):
        json_data = json.dumps(data)
        with self.lock:
            if self.socket:
                try:
                    self.socket.sendall(json_data.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError, OSError) as e:
                    print(f"Error sending data: {e}. Attempting to reconnect...")
                    self.connected = False
                    if self.socket:
                        self.socket.close()
                        self.socket = None  # Asegura que el socket se reinicie en el siguiente ciclo

    def receive_json(self):
        try:
            data = self.socket.recv(1024)
            if not data:
                return None
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
            return None

    def authenticate(self):
        auth_message = {"auth": SECRET_KEY}
        self.send_json(auth_message)
        response = self.receive_json()
        return response and response.get("status") == "ok"

    def connect(self, port, mode):
        while True:
            try:
                if self.socket:
                    try:
                        self.socket.close()
                    except OSError:
                        pass  # Handle the case where socket close raises an error
                    self.socket = None

                self.socket = self.create_socket()
                self.socket.connect((self.server_host, port))
                self.socket.settimeout(TIMEOUT)
                print(f"{self.name} connected to server at {self.server_host}:{port} for {mode}")
                if not self.authenticate():
                    print("Authentication failed. Retrying...")
                    self.socket.close()
                    time.sleep(CHECK_INTERVAL)
                    continue

                self.connected = True
                if mode == "sending":
                    self.sending_loop()
                elif mode == "receiving":
                    self.receiving_loop()
            except socket.gaierror as e:
                print(f"Name resolution error: {e}. Retrying in {CHECK_INTERVAL} seconds...")
                self.connected = False
                time.sleep(2 * CHECK_INTERVAL)
            except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError, TimeoutError, OSError) as e:
                print(f"Connection failed: {e}. Retrying in {CHECK_INTERVAL} seconds...")
                self.connected = False
                time.sleep(CHECK_INTERVAL)
            finally:
                if self.socket:
                    try:
                        self.socket.close()
                    except OSError:
                        pass  # Handle the case where socket close raises an error
                    self.socket = None  # Ensure the socket is reset in the next loop


    def sending_loop(self):
        while self.connected:
            message = {
                "sender": self.name,
                "message": f"Hello from {self.name}",
                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y:%m:%d %H:%M:%S')
            }
            try:
                self.send_json(message)
            except (ConnectionResetError, BrokenPipeError, OSError):
                print(f"Connection failed. Retrying...")
                self.connected = False
            time.sleep(CHECK_INTERVAL)

    def receiving_loop(self):
        while self.connected:
            response = self.receive_json()
            if response is None:
                print("No response from server, reconnecting...")
                self.connected = False
            else:
                print(f"Received from server: {response}")
                self.handle_received_message(response)
            time.sleep(CHECK_INTERVAL)

    def handle_received_message(self, message):
        print(f"Processing received message: {message}")
        # Aquí podrías agregar lógica para responder de manera personalizada

    def start(self):
        threading.Thread(target=self.connect, args=(self.send_port, "sending")).start()
        threading.Thread(target=self.connect, args=(self.receive_port, "receiving")).start()

def custom_message_sender(hexapod):
    while True:
        if hexapod.connected:
            message = {
                "sender": hexapod.name,
                "command": "MOVE_FORWARD",
                "parameters": {"speed": 5, "duration": 10},
                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y:%m:%d %H:%M:%S')
            }
            hexapod.send_json(message)
        time.sleep(2)
