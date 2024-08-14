import threading
import time
import datetime
from socket_utils import create_socket, send_json, receive_json, authenticate

TIMEOUT = 1  # Seconds to wait for a response before retrying connection
CHECK_INTERVAL = 0.5  # Seconds

def client_thread(client_name, server_host, port, mode):
    while True:
        client_socket = None
        try:
            client_socket = create_socket()
            client_socket.connect((server_host, port))
            client_socket.settimeout(TIMEOUT)
            print(f"{client_name} connected to server at {server_host}:{port} for {mode}")

            if not authenticate(client_socket):
                print("Authentication with server failed. Retrying...")
                client_socket.close()
                time.sleep(CHECK_INTERVAL)
                continue

            if mode == "sending":
                while True:
                    message = {
                        "sender": client_name,
                        "message": f"Hello from {client_name}",
                        "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y:%m:%d %H:%M:%S')
                    }
                    try:
                        send_json(client_socket, message)
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"Connection to {server_host} for sending failed. Retrying...")
                        break
                    time.sleep(CHECK_INTERVAL)
            elif mode == "receiving":
                while True:
                    response = receive_json(client_socket)
                    if response is None:
                        print(f"No response from server, reconnecting...")
                        break
                    print(f"Received from server: {response}")
                    time.sleep(CHECK_INTERVAL)

        except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError, TimeoutError) as e:
            print(f"Connection to {server_host} for {mode} failed: {e}. Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

        finally:
            if client_socket:
                client_socket.close()
