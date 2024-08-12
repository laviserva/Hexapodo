import threading
import socket
import queue
import time
from server import server_thread
from client import client_thread

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433

def send_predefined_messages_after_connection(client_name, send_queue):
    # Esperar un tiempo para asegurar que la conexión esté establecida
    time.sleep(5)  # Ajusta este tiempo según sea necesario

    # Lista de mensajes a enviar
    messages = [
        {"sender": client_name, "message": "mueve 1", "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')},
        {"sender": client_name, "message": "mueve 2", "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')},
        {"sender": client_name, "message": "mueve 3", "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
    ]

    for message in messages:
        send_queue.put(message)
        time.sleep(2)  # Esperar dos segundos entre cada mensaje

if __name__ == "__main__":
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    send_queue = queue.Queue()

    # Iniciar hilos para servidor y cliente
    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_SEND_PORT, "sending")).start()
    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_RECEIVE_PORT, "receiving")).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_RECEIVE_PORT, "sending", send_queue)).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_SEND_PORT, "receiving", queue.Queue())).start()

    # Enviar mensajes predefinidos después de que la conexión esté establecida
    send_predefined_messages_after_connection(client_name, send_queue)
