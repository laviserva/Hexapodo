from socket_utils import create_socket, send_json, receive_json, authenticate
import time

def client_thread(client_name, server_host, port, mode, message_queue):
    while True:
        client_socket = None
        try:
            client_socket = create_socket()
            client_socket.connect((server_host, port))
            client_socket.settimeout(None)  # No timeout, keep the connection open
            print(f"{client_name} connected to server at {server_host}:{port} for {mode}")

            if not authenticate(client_socket):
                print("Authentication with server failed. Retrying...")
                client_socket.close()
                time.sleep(0.5)
                continue

            if mode == "sending":
                while True:
                    if not message_queue.empty():
                        message = message_queue.get()
                        try:
                            send_json(client_socket, message)
                            response = receive_json(client_socket)
                            if response:
                                print(f"Server response: {response}")
                        except (ConnectionResetError, BrokenPipeError):
                            print(f"Connection to {server_host} for sending failed. Retrying...")
                            break
                    time.sleep(0.1)
            elif mode == "receiving":
                while True:
                    response = receive_json(client_socket)
                    if response is None:
                        print(f"No response from server, reconnecting...")
                        break
                    print(f"Received from server: {response}")
                    time.sleep(0.1)

        except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError) as e:
            print(f"Connection to {server_host} for {mode} failed: {e}. Retrying in 0.5 seconds...")
            time.sleep(0.5)

        finally:
            if client_socket:
                client_socket.close()
