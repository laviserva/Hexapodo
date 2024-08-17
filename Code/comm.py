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
    # Send authentication message
    auth_message = {"auth": SECRET_KEY}
    send_json(sock, auth_message)
    # Receive response
    response = receive_json(sock)
    if response and response.get("status") == "ok":
        return True
    return False

def handle_client(sock, addr):
    try:
        # Receive the initial message which should be the authentication message
        auth_message = receive_json(sock)
        if not auth_message or auth_message.get("auth") != SECRET_KEY:
            print(f"Authentication failed for {addr}. Closing connection.")
            send_json(sock, {"status": "error", "message": "Authentication failed"})
            sock.close()
            return
        
        # Send authentication success response
        send_json(sock, {"status": "ok", "message": "Authenticated successfully"})
        
        while True:
            data = receive_json(sock)
            if data is None:
                break
            print(f"Received from {addr}: {data}")
            send_json(sock, data)  # Echo the received data back to the client
        
    
    finally:
        sock.close()
        print(f"Connection with {addr} closed.")

def server_thread(server_name, port, mode):
    server_socket = create_socket()
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"{server_name} is listening on port {port} for {mode}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{mode.capitalize()} connection from {client_address} has been established.")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def client_thread(client_name, server_host, port, mode):
    while True:
        client_socket = None
        try:
            client_socket = create_socket()
            client_socket.connect((server_host, port))
            client_socket.settimeout(TIMEOUT)  # Set timeout for receiving data
            print(f"{client_name} connected to server at {server_host}:{port} for {mode}")

            # Authenticate with the server
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

if __name__ == "__main__":
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_SEND_PORT, "sending")).start()
    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_RECEIVE_PORT, "receiving")).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_RECEIVE_PORT, "sending")).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_SEND_PORT, "receiving")).start()

