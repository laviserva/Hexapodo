import threading
import socket
import random
import time

# Configuración de puertos
SYNC_PORT = 65426  # Puerto utilizado para la sincronización inicial
DATA_PORT = 65427  # Puerto utilizado para el intercambio de datos

# Determinación del nombre de la Raspberry Pi (hexápodo)
raspberrypi_name = socket.gethostname()

# Configuración dinámica basada en el nombre de host
if raspberrypi_name == 'hexapodo1':
    server_host = 'hexapodo2.local'
    client_name = 'hexapodo1.local'
elif raspberrypi_name == 'hexapodo2':
    server_host = 'hexapodo1.local'
    client_name = 'hexapodo2.local'
else:
    raise ValueError("Nombre de host no reconocido. Asegúrate de que el nombre de host sea 'hexapodo1' o 'hexapodo2'.")

# Definir las variables globales para almacenar los resultados
hexapod1_result = None
hexapod2_result = None

def wait_for_other_hexapod():
    if raspberrypi_name == 'hexapodo1':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sync_sock:
            sync_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sync_sock.bind((client_name, SYNC_PORT))
            sync_sock.listen(1)
            print(f"{client_name} esperando conexión de sincronización...")
            conn, addr = sync_sock.accept()
            with conn:
                print(f"{client_name} conectado con {addr} para sincronización.")
                conn.sendall(b'ready')
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sync_sock:
            sync_sock.connect((server_host, SYNC_PORT))
            print(f"{client_name} conectado con {server_host} para sincronización.")
            data = sync_sock.recv(1024)
            print(f"{client_name} recibió un mensaje de sincronización: {data.decode('utf-8')}")

def exchange_data(result):
    if raspberrypi_name == 'hexapodo1':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
            data_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data_sock.bind((client_name, DATA_PORT))
            data_sock.listen(1)
            print(f"{client_name} esperando conexión de datos...")
            conn, addr = data_sock.accept()
            with conn:
                print(f"{client_name} conectado con {addr} para intercambio de datos.")
                conn.sendall(str(result).encode('utf-8'))
                received_data = conn.recv(1024)
                return int(received_data.decode('utf-8'))
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
            time.sleep(1)  # Esperar un breve momento para asegurar que el servidor esté listo
            data_sock.connect((server_host, DATA_PORT))
            print(f"{client_name} conectado con {server_host} para intercambio de datos.")
            data_sock.sendall(str(result).encode('utf-8'))
            received_data = data_sock.recv(1024)
            return int(received_data.decode('utf-8'))

def hexapod_task():
    global hexapod1_result, hexapod2_result
    
    wait_for_other_hexapod()
    
    for i in range(3):  # Repetimos el proceso 3 veces
        print(f"--- Iteración {i + 1} ---")
        result = random.randint(1, 100) + random.randint(1, 100)
        print(f"{client_name} realizó una suma y el resultado es {result}")
        
        # Intercambio de datos usando TCP
        received_result = exchange_data(result)
        print(f"{client_name} recibió el resultado: {received_result}")

        # Asignar resultados recibidos
        if raspberrypi_name == 'hexapodo1':
            hexapod1_result = result
            hexapod2_result = received_result
        else:
            hexapod2_result = result
            hexapod1_result = received_result
        
        print(f"{client_name} intercambio completo para iteración {i + 1}. Resultado de hexapodo1: {hexapod1_result}, Resultado de hexapodo2: {hexapod2_result}")
        time.sleep(1)  # Pausa para ver claramente la iteración
    
    print(f"{client_name} ha terminado el intercambio de información.")

def main():
    hexapod_thread = threading.Thread(target=hexapod_task)
    hexapod_thread.start()
    hexapod_thread.join()

    print("El intercambio de información ha finalizado.")

if __name__ == "__main__":
    main()
