import threading
import socket
import random
import json
import time

class HexapodoComunicator:
    def __init__(self, client_name, server_host, sync_port=65426, data_port=65427):
        self.client_name = client_name
        self.server_host = server_host
        self.sync_port = sync_port
        self.data_port = data_port
        self.hexapod1_result = None
        self.hexapod2_result = None
        self.raspberrypi_name = socket.gethostname()

    def wait_for_other_hexapod(self):
        if self.raspberrypi_name == 'hexapodo1':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sync_sock:
                sync_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sync_sock.bind((self.client_name, self.sync_port))
                sync_sock.listen(1)
                print(f"{self.client_name} esperando conexión de sincronización...")
                conn, addr = sync_sock.accept()
                with conn:
                    print(f"{self.client_name} conectado con {addr} para sincronización.")
                    conn.sendall(b'ready')
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sync_sock:
                sync_sock.connect((self.server_host, self.sync_port))
                print(f"{self.client_name} conectado con {self.server_host} para sincronización.")
                data = sync_sock.recv(1024)
                print(f"{self.client_name} recibió un mensaje de sincronización: {data.decode('utf-8')}")

    def exchange_data(self, message):
        if self.raspberrypi_name == 'hexapodo1':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
                data_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                data_sock.bind((self.client_name, self.data_port))
                data_sock.listen(1)
                print(f"{self.client_name} esperando conexión de datos...")
                conn, addr = data_sock.accept()
                with conn:
                    print(f"{self.client_name} conectado con {addr} para intercambio de datos.")
                    conn.sendall(json.dumps(message).encode('utf-8'))
                    received_data = conn.recv(1024)
                    return json.loads(received_data.decode('utf-8'))
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
                time.sleep(1)
                data_sock.connect((self.server_host, self.data_port))
                print(f"{self.client_name} conectado con {self.server_host} para intercambio de datos.")
                data_sock.sendall(json.dumps(message).encode('utf-8'))
                received_data = data_sock.recv(1024)
                return json.loads(received_data.decode('utf-8'))

    def execute_task(self, iterations=3):
        self.wait_for_other_hexapod()
        
        for i in range(iterations):
            print(f"--- Iteración {i + 1} ---")
            result = random.randint(1, 100) + random.randint(1, 100)
            message = {"iteracion": i + 1, "resultado": result}
            print(f"{self.client_name} envía el mensaje: {message}")
            
            received_message = self.exchange_data(message)
            print(f"{self.client_name} recibió el mensaje: {received_message}")

            if self.raspberrypi_name == 'hexapodo1':
                self.hexapod1_result = result
                self.hexapod2_result = received_message["resultado"]
            else:
                self.hexapod2_result = result
                self.hexapod1_result = received_message["resultado"]
            
            print(f"{self.client_name} intercambio completo para iteración {i + 1}. Resultado de hexapodo1: {self.hexapod1_result}, Resultado de hexapodo2: {self.hexapod2_result}")
            time.sleep(1)
        
        print(f"{self.client_name} ha terminado el intercambio de información.")
