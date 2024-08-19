import socket
import random
import time
import json

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433

raspberrypi_name = socket.gethostname()
if raspberrypi_name == 'hexapodo1':
    server_host = 'hexapodo2.local'
    client_name = 'hexapodo1.local'
else:
    server_host = 'hexapodo1.local'
    client_name = 'hexapodo2.local'

def send_json(connection, message):
    json_data = json.dumps(message)
    connection.sendall(json_data.encode('utf-8'))

def receive_json(connection):
    data = b''
    while True:
        packet = connection.recv(1024)
        if not packet:
            break
        data += packet
    return json.loads(data.decode('utf-8'))

def send_custom_message(client_name, server_host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, port))
        print(f"Conectado a {server_host}:{port} desde {client_name}")
        while True:
            message = "holAS"  # Aquí podrías cambiar el mensaje según sea necesario
            send_json(s, message)
            print(f"Mensaje enviado: {message}")
            time.sleep(random.random())  # Simulación de espera entre mensajes

def receive_custom_message(server_host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_host, port))
        s.listen()
        print(f"Servidor escuchando en {server_host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión establecida con {addr}")
                while True:
                    message = receive_json(conn)
                    if message:
                        print(f"Mensaje recibido: {message}")
                    else:
                        break

# Inicia el proceso de envío y recepción

send_custom_message(client_name, server_host, SERVER_SEND_PORT)
receive_custom_message(server_host, SERVER_RECEIVE_PORT)
