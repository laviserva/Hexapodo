import socket
import threading
import time
import json
import datetime

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433
CHECK_INTERVAL = 0.5  # Seconds
TIMEOUT = 1  # Seconds to wait for a response before retrying connection
SECRET_KEY = "my_secret_key"  # Shared secret for basic authentication

# Singleton for socket creation
class SocketFactory:
    _instance = None

    @staticmethod
    def get_instance():
        if SocketFactory._instance is None:
            SocketFactory._instance = SocketFactory()
        return SocketFactory._instance

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Strategy pattern for sending and receiving JSON
class CommunicationStrategy:
    def send_json(self, sock, data):
        json_data = json.dumps(data)
        sock.sendall(json_data.encode('utf-8'))

    def receive_json(self, sock):
        try:
            data = sock.recv(1024)
            if not data:
                return None
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
            return None

# Strategy pattern for authentication
class AuthenticationStrategy:
    def authenticate(self, sock):
        # Send authentication message
        auth_message = {"auth": SECRET_KEY}
        CommunicationStrategy().send_json(sock, auth_message)
        # Receive response
        response = CommunicationStrategy().receive_json(sock)
        if response and response.get("status") == "ok":
            return True
        return False

# Observer pattern for handling clients
class ClientHandler:
    def __init__(self):
        self.communication_strategy = CommunicationStrategy()

    def handle_client(self, sock, addr):
        try:
            # Receive the initial message which should be the authentication message
            auth_message = self.communication_strategy.receive_json(sock)
            if not auth_message or auth_message.get("auth") != SECRET_KEY:
                print(f"Authentication failed for {addr}. Closing connection.")
                self.communication_strategy.send_json(sock, {"status": "error", "message": "Authentication failed"})
                sock.close()
                return

            # Send authentication success response
            self.communication_strategy.send_json(sock, {"status": "ok", "message": "Authenticated successfully"})

            while True:
                data = self.communication_strategy.receive_json(sock)
                if data is None:
                    break
                print(f"Received from {addr}: {data}")
                self.communication_strategy.send_json(sock, data)  # Echo the received data back to the client

        finally:
            sock.close()
            print(f"Connection with {addr} closed.")

# Server and client threads
class ServerThread(threading.Thread):
    def __init__(self, server_name, port, mode):
        super().__init__()
        self.server_name = server_name
        self.port = port
        self.mode = mode
        self.socket_factory = SocketFactory.get_instance()
        self.client_handler = ClientHandler()

    def run(self):
        server_socket = self.socket_factory.create_socket()
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(5)
        print(f"{self.server_name} is listening on port {self.port} for {self.mode}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"{self.mode.capitalize()} connection from {client_address} has been established.")
            threading.Thread(target=self.client_handler.handle_client, args=(client_socket, client_address)).start()

class ClientThread(threading.Thread):
    def __init__(self, client_name, server_host, port, mode):
        super().__init__()
        self.client_name = client_name
        self.server_host = server_host
        self.port = port
        self.mode = mode
        self.socket_factory = SocketFactory.get_instance()
        self.communication_strategy = CommunicationStrategy()
        self.authentication_strategy = AuthenticationStrategy()

    def run(self):
        while True:
            client_socket = None
            try:
                client_socket = self.socket_factory.create_socket()
                client_socket.connect((self.server_host, self.port))
                client_socket.settimeout(TIMEOUT)  # Set timeout for receiving data
                print(f"{self.client_name} connected to server at {self.server_host}:{self.port} for {self.mode}")

                # Authenticate with the server
                if not self.authentication_strategy.authenticate(client_socket):
                    print("Authentication with server failed. Retrying...")
                    client_socket.close()
                    time.sleep(CHECK_INTERVAL)
                    continue

                if self.mode == "sending":
                    while True:
                        message = {
                            "sender": self.client_name,
                            "message": f"Hello from {self.client_name}",
                            "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y:%m:%d %H:%M:%S')
                        }
                        try:
                            self.communication_strategy.send_json(client_socket, message)
                        except (ConnectionResetError, BrokenPipeError):
                            print(f"Connection to {self.server_host} for sending failed. Retrying...")
                            break
                        time.sleep(CHECK_INTERVAL)
                elif self.mode == "receiving":
                    while True:
                        response = self.communication_strategy.receive_json(client_socket)
                        if response is None:
                            print(f"No response from server, reconnecting...")
                            break
                        print(f"Received from server: {response}")
                        time.sleep(CHECK_INTERVAL)

            except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError, TimeoutError) as e:
                print(f"Connection to {self.server_host} for {self.mode} failed: {e}. Retrying in {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

            finally:
                if client_socket:
                    client_socket.close()

if __name__ == "__main__":
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    ServerThread(raspberrypi_name, SERVER_SEND_PORT, "sending").start()
    ServerThread(raspberrypi_name, SERVER_RECEIVE_PORT, "receiving").start()
    ClientThread(client_name, server_host, SERVER_RECEIVE_PORT, "sending").start()
    ClientThread(client_name, server_host, SERVER_SEND_PORT, "receiving").start()