import threading
from socket_utils import create_socket, receive_json, send_json, SECRET_KEY

def handle_client(sock, addr):
    try:
        auth_message = receive_json(sock)
        if not auth_message or auth_message.get("auth") != SECRET_KEY:
            print(f"Authentication failed for {addr}. Closing connection.")
            send_json(sock, {"status": "error", "message": "Authentication failed"})
            sock.close()
            return
        
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
