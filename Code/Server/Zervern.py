import threading
from socket_utils import create_socket, receive_json, send_json, SECRET_KEY
import json

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
            datazz = receive_json(sock)
            if datazz is None:
                print(f"Connection lost or empty message from {addr}.")
                break
            datazz["message"] = json.loads(datazz["message"]) 
            print(f"Received from {addr}: {datazz}")
            #print(data["message"], type(data["message"]))

            # Validar que el mensaje tenga la estructura esperada
            message_type = datazz.get("type", "unknown")
            if message_type == "state":
                if "data" in datazz["message"]:
                    print(f"Processing state: {datazz['message']['data']}")
                    send_json(sock, {"status": "received", "data": datazz["message"]["data"]})
                else:
                    print(f"Malformed message: 'data' field is missing in state message")
                    send_json(sock, {"status": "error", "message": "Malformed state message"})
            elif message_type == "ack":
                print(f"Acknowledgement received from {addr}")
                send_json(sock, {"status": "ack_received"})
            else:
                print(f"Unknown message type: {message_type}")
                send_json(sock, {"status": "error", "message": "Unknown message type"})

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    
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
